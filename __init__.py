# -*- coding: utf-8 -*-

def classFactory(iface):
    from .geoprompt_plugin import GeoPromptPlugin
    return GeoPromptPlugin(iface)
