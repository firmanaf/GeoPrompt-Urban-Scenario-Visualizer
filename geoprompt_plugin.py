# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
import os

from .geoprompt_dock import GeoPromptDock


class GeoPromptPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dock = None
        self.toolbar = None

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "resources", "icons", "geoprompt_icon.svg")
        self.action = QAction(QIcon(icon_path), "GeoPrompt Urban Scenario Visualizer", self.iface.mainWindow())
        self.action.triggered.connect(self.show_dock)
        self.iface.addPluginToMenu("&GeoPrompt Urban Scenario Visualizer", self.action)
        self.toolbar = self.iface.addToolBar("GeoPrompt")
        self.toolbar.setObjectName("GeoPromptToolbar")
        self.toolbar.addAction(self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginMenu("&GeoPrompt Urban Scenario Visualizer", self.action)
            if self.toolbar:
                self.toolbar.removeAction(self.action)
        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock = None
        if self.toolbar:
            del self.toolbar
            self.toolbar = None

    def show_dock(self):
        if self.dock is None:
            self.dock = GeoPromptDock(self.iface, self.iface.mainWindow())
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.show()
        self.dock.raise_()
