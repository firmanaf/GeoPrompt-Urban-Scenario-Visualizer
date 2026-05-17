# -*- coding: utf-8 -*-
from qgis.core import QgsMapSettings, QgsMapRendererCustomPainterJob, QgsRectangle
from qgis.PyQt.QtCore import QSize, Qt, QRect
from qgis.PyQt.QtGui import QImage, QPainter, QColor


def _content_box_for_padding(extent: QgsRectangle, width: int, height: int):
    target_ratio = width / float(height)
    extent_ratio = extent.width() / float(extent.height()) if extent.height() else target_ratio
    if extent_ratio >= target_ratio:
        content_w = width
        content_h = max(1, int(round(width / extent_ratio)))
        xoff = 0
        yoff = int(round((height - content_h) / 2.0))
    else:
        content_h = height
        content_w = max(1, int(round(height * extent_ratio)))
        yoff = 0
        xoff = int(round((width - content_w) / 2.0))
    return {
        "xoff": xoff,
        "yoff": yoff,
        "width": content_w,
        "height": content_h,
        "target_width": width,
        "target_height": height,
    }


def export_canvas_extent_to_png(iface, extent: QgsRectangle, out_png: str, width: int, height: int, pad_to_aspect: bool = True):
    canvas = iface.mapCanvas()
    crs = canvas.mapSettings().destinationCrs()

    if pad_to_aspect:
        content = _content_box_for_padding(extent, width, height)
        render_w = content["width"]
        render_h = content["height"]
    else:
        content = {"xoff": 0, "yoff": 0, "width": width, "height": height, "target_width": width, "target_height": height}
        render_w = width
        render_h = height

    settings = QgsMapSettings(canvas.mapSettings())
    settings.setOutputSize(QSize(render_w, render_h))
    settings.setExtent(QgsRectangle(extent))
    settings.setBackgroundColor(QColor(255, 255, 255, 255))
    settings.setLayers(canvas.layers())

    rendered = QImage(render_w, render_h, QImage.Format_ARGB32_Premultiplied)
    rendered.fill(Qt.white)
    painter = QPainter(rendered)
    job = QgsMapRendererCustomPainterJob(settings, painter)
    job.start()
    job.waitForFinished()
    painter.end()

    final_img = QImage(width, height, QImage.Format_ARGB32_Premultiplied)
    final_img.fill(Qt.white)
    painter2 = QPainter(final_img)
    painter2.drawImage(QRect(content["xoff"], content["yoff"], render_w, render_h), rendered)
    painter2.end()

    if not final_img.save(out_png, "PNG"):
        raise RuntimeError(f"Failed to save exported canvas PNG: {out_png}")

    return {
        "crs": crs,
        "original_extent": QgsRectangle(extent),
        "content_box": content,
        "padded": bool(pad_to_aspect and (content["xoff"] > 0 or content["yoff"] > 0)),
        "image_size": (width, height),
    }
