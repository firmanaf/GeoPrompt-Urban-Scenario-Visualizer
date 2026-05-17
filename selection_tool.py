# -*- coding: utf-8 -*-
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsWkbTypes, QgsRectangle, QgsPointXY
from qgis.PyQt.QtCore import Qt, pyqtSignal
from qgis.PyQt.QtGui import QColor


class RectangleSelectionTool(QgsMapTool):
    rectangleSelected = pyqtSignal(object)

    def __init__(self, canvas):
        super().__init__(canvas)
        self.canvas = canvas
        self.start_point = None
        self.lock_aspect = True
        self.aspect_ratio = 1536.0 / 1024.0
        self.rubber = QgsRubberBand(canvas, QgsWkbTypes.PolygonGeometry)
        self.rubber.setColor(QColor(0, 180, 190, 70))
        self.rubber.setStrokeColor(QColor(0, 120, 180, 230))
        self.rubber.setWidth(2)

    def set_lock_aspect(self, enabled: bool):
        self.lock_aspect = bool(enabled)

    def set_aspect_ratio(self, width: int, height: int):
        if width and height and height > 0:
            self.aspect_ratio = float(width) / float(height)

    def canvasPressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        self.start_point = self.toMapCoordinates(event.pos())
        self.rubber.reset(QgsWkbTypes.PolygonGeometry)

    def canvasMoveEvent(self, event):
        if self.start_point is None:
            return
        current = self.toMapCoordinates(event.pos())
        self._show_rect_from_points(self.start_point, current)

    def canvasReleaseEvent(self, event):
        if self.start_point is None:
            return
        end_point = self.toMapCoordinates(event.pos())
        rect = self._rect_from_points(self.start_point, end_point)
        self.start_point = None
        if rect.width() > 0 and rect.height() > 0:
            self._show_rect(rect)
            self.rectangleSelected.emit(rect)

    def _rect_from_points(self, p1, p2):
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()
        dx = x2 - x1
        dy = y2 - y1
        if self.lock_aspect and abs(dx) > 0 and abs(dy) > 0:
            sx = 1 if dx >= 0 else -1
            sy = 1 if dy >= 0 else -1
            abs_dx = abs(dx)
            abs_dy = abs(dy)
            current_ratio = abs_dx / abs_dy if abs_dy else self.aspect_ratio
            if current_ratio >= self.aspect_ratio:
                abs_dy = abs_dx / self.aspect_ratio
            else:
                abs_dx = abs_dy * self.aspect_ratio
            x2 = x1 + sx * abs_dx
            y2 = y1 + sy * abs_dy
        xmin, xmax = sorted([x1, x2])
        ymin, ymax = sorted([y1, y2])
        return QgsRectangle(xmin, ymin, xmax, ymax)

    def _show_rect_from_points(self, p1, p2):
        self._show_rect(self._rect_from_points(p1, p2))

    def _show_rect(self, rect):
        xmin, xmax = rect.xMinimum(), rect.xMaximum()
        ymin, ymax = rect.yMinimum(), rect.yMaximum()
        self.rubber.reset(QgsWkbTypes.PolygonGeometry)
        self.rubber.addPoint(QgsPointXY(xmin, ymin), False)
        self.rubber.addPoint(QgsPointXY(xmax, ymin), False)
        self.rubber.addPoint(QgsPointXY(xmax, ymax), False)
        self.rubber.addPoint(QgsPointXY(xmin, ymax), False)
        self.rubber.addPoint(QgsPointXY(xmin, ymin), True)
        self.rubber.show()

    def deactivate(self):
        self.rubber.hide()
        super().deactivate()
