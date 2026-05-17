# -*- coding: utf-8 -*-
import os
import re
import time
from osgeo import gdal, osr
from qgis.core import QgsProject, QgsRasterLayer


def _slugify(text: str) -> str:
    text = (text or "geoprompt").lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text[:48] or "geoprompt"


def write_image_bytes_as_geotiff(image_bytes: bytes, extent, crs, output_folder: str, prompt: str, model: str) -> str:
    if not image_bytes:
        raise RuntimeError("Image result is empty.")
    os.makedirs(output_folder, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_tif = os.path.join(output_folder, f"geoprompt_{ts}_{_slugify(prompt)}.tif")

    vsimem = f"/vsimem/geoprompt_{int(time.time() * 1000)}.png"
    try:
        gdal.FileFromMemBuffer(vsimem, bytes(image_bytes))
        src = gdal.Open(vsimem)
        if src is None:
            raise RuntimeError("GDAL cannot open generated image bytes. Make sure the provider output is a valid PNG/JPEG image.")

        w, h = src.RasterXSize, src.RasterYSize
        bands = min(src.RasterCount, 4)
        if bands < 1:
            raise RuntimeError("Generated image has no raster bands.")

        driver = gdal.GetDriverByName("GTiff")
        dst = driver.Create(out_tif, w, h, bands, gdal.GDT_Byte, options=["COMPRESS=LZW", "TILED=YES"])
        if dst is None:
            raise RuntimeError(f"Cannot create output GeoTIFF: {out_tif}")

        xmin, xmax = extent.xMinimum(), extent.xMaximum()
        ymin, ymax = extent.yMinimum(), extent.yMaximum()
        dst.SetGeoTransform((xmin, (xmax - xmin) / w, 0, ymax, 0, -(ymax - ymin) / h))

        srs = osr.SpatialReference()
        if crs and crs.isValid():
            authid = crs.authid()
            if authid and authid.upper().startswith("EPSG:"):
                srs.ImportFromEPSG(int(authid.split(":")[1]))
            else:
                srs.ImportFromWkt(crs.toWkt())
            dst.SetProjection(srs.ExportToWkt())

        dst.SetMetadataItem("GEOPROMPT_PROMPT", prompt[:8000])
        dst.SetMetadataItem("GEOPROMPT_MODEL", model)
        dst.SetMetadataItem("GEOPROMPT_WARNING", "AI-generated scenario visualization, not official spatial data, not valid for legal delineation or measurement.")
        dst.SetMetadataItem("GEOPROMPT_EXTENT", f"{xmin},{ymin},{xmax},{ymax}")
        dst.SetMetadataItem("GEOPROMPT_CRS", crs.authid() if crs and crs.isValid() else "unknown")
        dst.SetMetadataItem("GEOPROMPT_CREATED_UTC", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

        for i in range(1, bands + 1):
            arr = src.GetRasterBand(i).ReadAsArray()
            band = dst.GetRasterBand(i)
            band.WriteArray(arr)
            if i == 4:
                band.SetColorInterpretation(gdal.GCI_AlphaBand)
        dst.FlushCache()
        dst = None
        src = None
    finally:
        gdal.Unlink(vsimem)
    return out_tif


def add_geotiff_to_project(path: str, prompt: str, iface=None, zoom_to_layer: bool = True):
    """
    Add GeoPrompt result directly to the QGIS Layers panel.

    Improvements:
    - Creates/uses a dedicated group.
    - Expands the group.
    - Places the newest result at the top of the group.
    - Sets the new raster as active layer.
    - Optionally zooms to the new layer and refreshes the canvas.
    """
    layer_name = "GeoPrompt_" + _slugify(prompt)[:28]
    layer = QgsRasterLayer(path, layer_name)
    if not layer.isValid():
        raise RuntimeError(f"GeoTIFF was created but failed to load into QGIS: {path}")

    project = QgsProject.instance()
    root = project.layerTreeRoot()

    group_name = "GeoPrompt Urban Scenarios"
    group = root.findGroup(group_name)
    if group is None:
        group = root.insertGroup(0, group_name)

    group.setExpanded(True)

    project.addMapLayer(layer, False)

    # Put newest layer at the top of the group.
    group.insertLayer(0, layer)

    # Make layer visible.
    node = group.findLayer(layer.id())
    if node is not None:
        node.setItemVisibilityChecked(True)

    if iface is not None:
        try:
            iface.setActiveLayer(layer)
        except Exception:
            pass

        if zoom_to_layer:
            try:
                iface.mapCanvas().setExtent(layer.extent())
            except Exception:
                pass

        try:
            iface.mapCanvas().refresh()
        except Exception:
            pass

        try:
            iface.layerTreeView().refreshLayerSymbology(layer.id())
        except Exception:
            pass

    return layer
