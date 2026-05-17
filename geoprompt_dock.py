# -*- coding: utf-8 -*-
import os
import tempfile
import traceback

from qgis.PyQt.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from qgis.core import QgsRectangle

from .prompt_presets import PROMPT_CATEGORIES
from .selection_tool import RectangleSelectionTool
from .canvas_exporter import export_canvas_extent_to_png
from .openai_image_client import edit_image_with_openai
from .gemini_image_client import edit_image_with_gemini
from .raster_writer import write_image_bytes_as_geotiff, add_geotiff_to_project
from .image_utils import crop_image_bytes


SIZE_MAP = {
    "Landscape 1536 x 1024": (1536, 1024, "1536x1024"),
    "Square 1024 x 1024": (1024, 1024, "1024x1024"),
    "Portrait 1024 x 1536": (1024, 1536, "1024x1536"),
    "Auto": (1024, 1024, "auto"),
}

PROVIDER_OPTIONS = [
    ("OpenAI", "openai"),
    ("Google Gemini Image", "gemini"),
]

OPENAI_MODEL_OPTIONS = [
    ("gpt-image-1.5  | recommended", "gpt-image-1.5"),
    ("gpt-image-1", "gpt-image-1"),
    ("gpt-image-1-mini | cheaper draft", "gpt-image-1-mini"),
    ("gpt-image-2 | if available", "gpt-image-2"),
    ("gpt-image-2-2026-04-21 | if available", "gpt-image-2-2026-04-21"),
    ("chatgpt-image-latest | requires verified organization", "chatgpt-image-latest"),
    ("dall-e-2 | legacy square only", "dall-e-2"),
    ("Custom model ID", "__custom__"),
]

GEMINI_MODEL_OPTIONS = [
    ("Gemini 2.5 Flash Image | gemini-2.5-flash-image", "gemini-2.5-flash-image"),
    ("Gemini 3 Pro Image Preview | gemini-3-pro-image-preview", "gemini-3-pro-image-preview"),
    ("Custom Gemini model ID", "__custom__"),
]


PRESERVE_GEOMETRY_APPENDIX = (
    "\n\nPreserve geometry mode is ON. "
    "Preserve the exact position, orientation, scale, and footprint of visible buildings, roads, rivers, shorelines, and block structure as much as possible. "
    "Do not move, rotate, crop, zoom in, zoom out, rescale, stretch, or redraw buildings into new locations. "
    "Preserve the full original frame, including edge features and map margins. "
    "Keep a top-down orthographic aerial/map view with the same apparent map scale as the input image. "
    "Apply only the requested urban planning scenario changes while maintaining spatial alignment with the original map image."
)


class GeoPromptDock(QDockWidget):
    def __init__(self, iface, parent=None):
        super().__init__("GeoPrompt Urban Scenario Visualizer", parent)
        self.iface = iface
        self.selected_extent = None
        self.selection_tool = RectangleSelectionTool(self.iface.mapCanvas())
        self.selection_tool.rectangleSelected.connect(self._on_rectangle_selected)
        self.setMinimumWidth(420)
        self.resize(500, 680)
        self._build_ui()
        self._sync_selection_ratio()

    def _section_label(self, text):
        label = QLabel(f"<b>{text}</b>")
        label.setStyleSheet("margin-top:4px; color:#1f2937;")
        return label

    def _make_info_box(self, title, body, color="#7a4a00", bg="#fff7e6", border="#f0c36d"):
        box = QFrame()
        box.setFrameShape(QFrame.NoFrame)
        box.setStyleSheet(
            f"QFrame {{background:{bg}; border:1px solid {border}; border-radius:5px; padding:4px;}}"
            "QLabel {border:0px; background:transparent;}"
        )
        layout = QVBoxLayout(box)
        layout.setContentsMargins(6, 5, 6, 5)
        layout.setSpacing(1)
        title_label = QLabel(f"<b>{title}</b>")
        title_label.setStyleSheet(f"color:{color};")
        body_label = QLabel(body)
        body_label.setWordWrap(True)
        body_label.setStyleSheet(f"color:{color};")
        layout.addWidget(title_label)
        layout.addWidget(body_label)
        return box

    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet("""
            QLabel { font-size: 8.6pt; }
            QLineEdit, QComboBox { min-height: 23px; padding-left: 4px; font-size: 8.6pt; }
            QPushButton { min-height: 24px; padding: 3px 8px; font-size: 8.6pt; }
            QTextEdit { font-size: 8.6pt; }
            QCheckBox { font-size: 8.6pt; spacing: 4px; }
        """)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(7, 7, 7, 7)
        layout.setSpacing(5)

        title = QLabel(
            "<span style='font-size:10.5pt; font-weight:700;'>GeoPrompt Urban Scenario Visualizer</span><br>"
            "<span style='color:#4b5563; font-size:7.3pt;'>AI-powered georeferenced urban scenario generation for QGIS</span><br>"
            "<span style='color:#0f766e; font-size:7.2pt; font-weight:600;'>Created by Firman Afrianto and Maya Safira</span>"
        )
        title.setWordWrap(True)
        layout.addWidget(title)

        form = QFormLayout()
        form.setHorizontalSpacing(7)
        form.setVerticalSpacing(4)

        self.provider = QComboBox()
        for label, provider_id in PROVIDER_OPTIONS:
            self.provider.addItem(label, provider_id)

        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.Password)
        self.api_key.setPlaceholderText("OpenAI: sk-... | Gemini: Google AI Studio API key")

        self.model = QComboBox()
        self._populate_models("openai")

        self.custom_model = QLineEdit()
        self.custom_model.setPlaceholderText("example: gpt-image-2 or a new OpenAI model ID")

        self.size = QComboBox()
        self.size.addItems(list(SIZE_MAP.keys()))
        self.size.currentTextChanged.connect(self._sync_selection_ratio)

        self.quality = QComboBox()
        self.quality.addItems(["default", "low", "medium", "high", "auto"])
        self.quality.setCurrentText("high")

        self.output_folder = QLineEdit()
        self.output_folder.setMinimumHeight(24)
        self.output_folder.setPlaceholderText("Select output folder")
        browse = QPushButton("Browse")
        browse.setMinimumHeight(24)
        browse.setFixedWidth(76)
        browse.clicked.connect(self._browse_folder)
        out_row = QHBoxLayout()
        out_row.setContentsMargins(0, 0, 0, 0)
        out_row.setSpacing(5)
        out_row.addWidget(self.output_folder, 1)
        out_row.addWidget(browse, 0)
        out_widget = QWidget()
        out_widget.setLayout(out_row)

        form.addRow("Provider", self.provider)
        form.addRow("API Key", self.api_key)
        form.addRow("Model", self.model)
        form.addRow("Custom model ID", self.custom_model)
        form.addRow("Output size", self.size)
        form.addRow("Quality", self.quality)
        form.addRow("Output folder", out_widget)
        layout.addLayout(form)

        layout.addWidget(self._section_label("Urban and Regional Planning Prompt Presets"))

        preset_form = QFormLayout()
        preset_form.setHorizontalSpacing(7)
        preset_form.setVerticalSpacing(4)
        self.category = QComboBox()
        self.category.addItems(list(PROMPT_CATEGORIES.keys()))
        self.category.currentTextChanged.connect(self._refresh_presets)
        self.preset = QComboBox()
        self.preset.currentIndexChanged.connect(self._apply_preset)
        preset_form.addRow("Category", self.category)
        preset_form.addRow("Preset", self.preset)
        layout.addLayout(preset_form)

        self.prompt = QTextEdit()
        self.prompt.setMinimumHeight(105)
        self.prompt.setPlaceholderText("Write an urban scenario prompt here...")
        layout.addWidget(self.prompt)

        layout.addWidget(self._make_info_box(
            "Important note",
            "The output is an AI-generated scenario visualization, not a legal map for measurement, delineation, or official classification. For best overlay alignment, use Select Area with locked aspect ratio and keep automatic padding off."
        ))

        layout.addWidget(self._section_label("Alignment and Georeferencing"))
        self.lock_ratio = QCheckBox("Lock selection to model output aspect ratio")
        self.lock_ratio.setChecked(True)
        self.lock_ratio.toggled.connect(self._sync_selection_ratio)

        self.auto_padding = QCheckBox("Use automatic padding when aspect ratio does not match (may cause slight reframing)")
        self.auto_padding.setChecked(False)

        self.preserve_geometry = QCheckBox("Preserve geometry mode")
        self.preserve_geometry.setChecked(True)

        self.use_current_canvas = QCheckBox("Use current canvas extent if no rectangle is selected")
        self.use_current_canvas.setChecked(True)

        self.auto_load_layer = QCheckBox("Load result directly into the Layers Panel")
        self.auto_load_layer.setChecked(True)

        self.zoom_to_result = QCheckBox("Automatically zoom to result")
        self.zoom_to_result.setChecked(False)

        for chk in [self.lock_ratio, self.auto_padding, self.preserve_geometry, self.use_current_canvas, self.auto_load_layer, self.zoom_to_result]:
            chk.setStyleSheet("margin-top:0px;")
            layout.addWidget(chk)

        self.ratio_label = QLabel("Aspect: -")
        self.ratio_label.setWordWrap(True)
        self.ratio_label.setStyleSheet("color:#4b5563; font-size:8.8pt;")
        layout.addWidget(self.ratio_label)

        row = QHBoxLayout()
        row.setSpacing(6)
        self.select_btn = QPushButton("Select Area")
        self.select_btn.clicked.connect(self.activate_selection_tool)
        self.canvas_btn = QPushButton("Use Current Canvas")
        self.canvas_btn.clicked.connect(self.use_canvas_extent)
        row.addWidget(self.select_btn)
        row.addWidget(self.canvas_btn)
        layout.addLayout(row)

        self.extent_label = QLabel("Selected extent: not selected yet")
        self.extent_label.setWordWrap(True)
        self.extent_label.setStyleSheet("color:#4b5563; font-size:8.8pt;")
        layout.addWidget(self.extent_label)

        self.generate_btn = QPushButton("Generate GeoPrompt Scenario")
        self.generate_btn.setMinimumHeight(32)
        self.generate_btn.setStyleSheet(
            "QPushButton {font-weight:bold; padding:5px; background:#0f766e; color:white; border-radius:5px;}"
            "QPushButton:disabled {background:#9ca3af; color:#f3f4f6;}"
        )
        self.generate_btn.clicked.connect(self.generate)
        layout.addWidget(self.generate_btn)

        self.status = QLabel("Siap.")
        self.status.setWordWrap(True)
        self.status.setStyleSheet(
            "QLabel {background:#f3f4f6; color:#374151; border:1px solid #d1d5db; "
            "border-radius:5px; padding:5px; font-size:8.2pt;}"
        )
        layout.addWidget(self.status)

        layout.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(root)
        self.setWidget(scroll)
        self.provider.currentIndexChanged.connect(self._on_provider_changed)
        self.model.currentIndexChanged.connect(self._on_model_changed)
        self._refresh_presets()
        self._on_provider_changed()
        self._on_model_changed()

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder:
            self.output_folder.setText(folder)

    def _refresh_presets(self):
        cat = self.category.currentText()
        self.preset.blockSignals(True)
        self.preset.clear()
        for p in PROMPT_CATEGORIES.get(cat, []):
            self.preset.addItem(p["label"], p)
        self.preset.blockSignals(False)
        self._apply_preset()

    def _apply_preset(self):
        p = self.preset.currentData()
        if p:
            self.prompt.setPlainText(p["prompt"])

    def _provider_id(self):
        return self.provider.currentData() or "openai"

    def _populate_models(self, provider_id):
        if not hasattr(self, "model"):
            return
        if provider_id == "gemini":
            options = GEMINI_MODEL_OPTIONS
        else:
            options = OPENAI_MODEL_OPTIONS
        self.model.blockSignals(True)
        self.model.clear()
        for label, model_id in options:
            self.model.addItem(label, model_id)
        self.model.setCurrentIndex(0)
        self.model.blockSignals(False)

    def _on_provider_changed(self):
        provider_id = self._provider_id()
        self._populate_models(provider_id)

        if provider_id == "gemini":
            self.api_key.setPlaceholderText("Google Gemini API key from Google AI Studio, or environment variable GOOGLE_API_KEY / GEMINI_API_KEY")
            self.custom_model.setPlaceholderText("example: gemini-2.5-flash-image or another Gemini image model")
            self.status.setText("Gemini provider is active. Use an API key from Google AI Studio.")
            self.quality.setEnabled(False)
        else:
            self.api_key.setPlaceholderText("sk-... or use the OPENAI_API_KEY environment variable")
            self.custom_model.setPlaceholderText("example: gpt-image-2 or a new OpenAI model ID")
            self.status.setText("OpenAI provider is active.")
            self.quality.setEnabled(True)

        self._on_model_changed()
        self._sync_selection_ratio()

    def _on_model_changed(self):
        model_id = self.model.currentData()
        provider_id = self._provider_id()
        self.custom_model.setVisible(model_id == "__custom__")

        if provider_id == "gemini":
            if model_id == "gemini-2.5-flash-image":
                self.status.setText("Gemini image is active: gemini-2.5-flash-image. The OpenAI quality setting is ignored for Gemini.")
            elif model_id == "gemini-3-pro-image-preview":
                self.status.setText("Gemini image pro is active if your API key has access. The OpenAI quality setting is ignored for Gemini.")
            else:
                self.status.setText("Gemini provider is active. The OpenAI quality setting is ignored for Gemini.")
        else:
            if model_id == "chatgpt-image-latest":
                self.status.setText("This model requires a verified organization on the OpenAI Platform. Use gpt-image-1.5 for a more stable setup.")
            elif model_id == "dall-e-2":
                self.status.setText("DALL·E 2 is a legacy edit model. The plugin automatically uses Square 1024 x 1024 output.")
            else:
                self.status.setText("Ready.")
        self._sync_selection_ratio()

    def _model_id(self):
        model_id = self.model.currentData()
        if model_id == "__custom__":
            model_id = self.custom_model.text().strip()
        return model_id or self.model.currentText().strip()

    def _current_size_tuple(self):
        model_id = self._model_id()
        if model_id == "dall-e-2":
            return (1024, 1024, "1024x1024")
        return SIZE_MAP[self.size.currentText()]

    def _sync_selection_ratio(self):
        if not hasattr(self, "selection_tool") or not hasattr(self, "lock_ratio"):
            return
        w, h, _ = self._current_size_tuple()
        self.selection_tool.set_aspect_ratio(w, h)
        self.selection_tool.set_lock_aspect(self.lock_ratio.isChecked())
        ratio = w / float(h)
        mode = "locked" if self.lock_ratio.isChecked() else "free"
        self.ratio_label.setText(f"Aspect: {w}:{h} ({ratio:.3f}) | selection mode: {mode} | best alignment: locked ratio + no padding")

    def activate_selection_tool(self):
        self._sync_selection_ratio()
        self.iface.mapCanvas().setMapTool(self.selection_tool)
        msg = "Drag a rectangle on the map canvas to select the scenario area."
        if self.lock_ratio.isChecked():
            msg += " The rectangle ratio is locked to the model output ratio."
        self.status.setText(msg)

    def _on_rectangle_selected(self, rect):
        self.selected_extent = rect
        self._update_extent_label(rect)
        self.status.setText("Area selected. Fill in the prompt and click Generate.")

    def use_canvas_extent(self):
        self.selected_extent = QgsRectangle(self.iface.mapCanvas().extent())
        self._update_extent_label(self.selected_extent)
        if self.auto_padding.isChecked():
            self.status.setText("Using current canvas extent. For best alignment, use Select Area with locked aspect ratio. Padding may slightly reframe the generated image.")

    def _update_extent_label(self, rect):
        ratio = rect.width() / rect.height() if rect and rect.height() else 0
        self.extent_label.setText(
            f"Selected extent: xmin={rect.xMinimum():.3f}, ymin={rect.yMinimum():.3f}, "
            f"xmax={rect.xMaximum():.3f}, ymax={rect.yMaximum():.3f} | rasio={ratio:.3f}"
        )

    def _api_key_value(self):
        manual = self.api_key.text().strip()
        if manual:
            return manual
        if self._provider_id() == "gemini":
            return os.environ.get("GOOGLE_API_KEY", "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()
        return os.environ.get("OPENAI_API_KEY", "").strip()

    def _final_prompt(self):
        prompt = self.prompt.toPlainText().strip()
        if self.preserve_geometry.isChecked():
            prompt += PRESERVE_GEOMETRY_APPENDIX
        return prompt

    def _friendly_error_message(self, error_text):
        low = error_text.lower()
        if "verified" in low and "organization" in low:
            return (
                "OpenAI error: this model requires organization verification.\n"
                "Quick fix: choose gpt-image-1.5, gpt-image-1, or gpt-image-1-mini."
            )
        if "permissiondenied" in low or "403" in low:
            return (
                "OpenAI error: access to this model is denied for the current API key or project.\n"
                "Try gpt-image-1.5 or check your OpenAI project access."
            )
        if "model" in low and ("not found" in low or "does not exist" in low or "not available" in low):
            return (
                "Model error: the selected model is not available for this API key or project.\n"
                "Choose another model or enter a valid custom model ID."
            )
        if "not_found" in low or "not found" in low or "not supported for generatecontent" in low:
            return (
                "Gemini error: the selected model is not available or does not support generateContent for this API key.\n"
                "Use Gemini 2.5 Flash Image. If using Gemini 3 Pro Image Preview, make sure your API key has access."
            )
        if "resource_exhausted" in low or "quota" in low or "free tier" in low or "rate limit" in low or "rate-limits" in low:
            return (
                "Gemini error: quota or rate limit has been exceeded, or this project has zero free-tier quota.\n"
                "Enable Gemini API billing, wait for quota reset, or switch to OpenAI."
            )
        if "google" in low or "gemini" in low:
            return (
                "Gemini provider error. Check your Google API key, model access in Google AI Studio, "
                "and make sure the google-genai package is installed."
            )
        if "api key" in low:
            return "API key error: the API key is empty or invalid. Check the API key for the selected provider."
        return f"Error: {error_text}"

    def generate(self):
        try:
            extent = self.selected_extent
            if extent is None and self.use_current_canvas.isChecked():
                extent = QgsRectangle(self.iface.mapCanvas().extent())
            if extent is None:
                QMessageBox.warning(self, "GeoPrompt", "Select an area first using Select Area, or enable current canvas extent.")
                return

            prompt = self._final_prompt()
            if not prompt:
                QMessageBox.warning(self, "GeoPrompt", "The prompt is empty.")
                return

            out_dir = self.output_folder.text().strip()
            if not out_dir:
                out_dir = QFileDialog.getExistingDirectory(self, "Select output folder")
                if not out_dir:
                    return
                self.output_folder.setText(out_dir)

            self.generate_btn.setEnabled(False)
            self.status.setText("1/4 Exporting QGIS canvas...")
            self.repaint()

            w, h, api_size = self._current_size_tuple()
            tmp_dir = tempfile.mkdtemp(prefix="geoprompt_")
            input_png = os.path.join(tmp_dir, "qgis_canvas.png")
            export_info = export_canvas_extent_to_png(
                self.iface,
                extent,
                input_png,
                w,
                h,
                pad_to_aspect=self.auto_padding.isChecked(),
            )

            provider_id = self._provider_id()
            model_id = self._model_id()

            if provider_id == "gemini":
                self.status.setText("2/4 Sending image and prompt to Google Gemini Image...")
                self.repaint()
                image_bytes = edit_image_with_gemini(
                    api_key=self._api_key_value(),
                    model=model_id,
                    input_png=input_png,
                    prompt=prompt,
                )
            else:
                self.status.setText("2/4 Sending image and prompt to OpenAI Image Edit API...")
                self.repaint()
                image_bytes = edit_image_with_openai(
                    api_key=self._api_key_value(),
                    model=model_id,
                    input_png=input_png,
                    prompt=prompt,
                    size=api_size,
                    quality=self.quality.currentText(),
                )

            if self.auto_padding.isChecked() and export_info.get("padded"):
                self.status.setText("2.5/4 Cropping the result to remove padding and preserve alignment...")
                self.repaint()
                image_bytes = crop_image_bytes(image_bytes, export_info["content_box"])

            self.status.setText("3/4 Writing result as a georeferenced GeoTIFF...")
            self.repaint()
            tif = write_image_bytes_as_geotiff(
                image_bytes,
                export_info["original_extent"],
                export_info["crs"],
                out_dir,
                prompt,
                f"{provider_id}:{model_id}",
            )

            if self.auto_load_layer.isChecked():
                self.status.setText("4/4 Loading result layer into the QGIS Layers Panel...")
                self.repaint()
                add_geotiff_to_project(tif, prompt, iface=self.iface, zoom_to_layer=self.zoom_to_result.isChecked())
                self.status.setText(f"Done. The layer has been loaded into the Layers Panel: {tif}")
                QMessageBox.information(self, "GeoPrompt", f"Scenario successfully generated and loaded into the QGIS Layers Panel:\n{tif}")
            else:
                self.status.setText(f"Done. GeoTIFF saved but not loaded automatically: {tif}")
                QMessageBox.information(self, "GeoPrompt", f"Scenario successfully generated:\n{tif}")

        except Exception as e:
            detail = traceback.format_exc()
            friendly = self._friendly_error_message(str(e))
            self.status.setText(friendly)
            QMessageBox.critical(self, "GeoPrompt Error", f"{friendly}\n\nDetail teknis:\n{detail[-1800:]}")
        finally:
            self.generate_btn.setEnabled(True)
