# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QByteArray, QBuffer, QIODevice
from qgis.PyQt.QtGui import QImage


def crop_image_bytes(image_bytes: bytes, content_box: dict, fmt: str = "PNG") -> bytes:
    """
    Crop generated image back to the original content area.

    The generated image may not always have the same pixel size as the submitted padded image,
    especially with non-OpenAI providers. Therefore the crop box is scaled from the submitted
    target_width/target_height to the actual returned image width/height.
    """
    if not image_bytes:
        raise RuntimeError("Image result is empty, cannot crop.")
    img = QImage.fromData(image_bytes)
    if img.isNull():
        raise RuntimeError("Failed to decode generated image for cropping.")

    target_w = int(content_box.get("target_width", img.width())) or img.width()
    target_h = int(content_box.get("target_height", img.height())) or img.height()

    sx = img.width() / float(target_w)
    sy = img.height() / float(target_h)

    xoff = int(round(float(content_box.get("xoff", 0)) * sx))
    yoff = int(round(float(content_box.get("yoff", 0)) * sy))
    w = int(round(float(content_box.get("width", img.width())) * sx))
    h = int(round(float(content_box.get("height", img.height())) * sy))

    xoff = max(0, min(xoff, img.width() - 1))
    yoff = max(0, min(yoff, img.height() - 1))
    w = max(1, min(w, img.width() - xoff))
    h = max(1, min(h, img.height() - yoff))

    cropped = img.copy(xoff, yoff, w, h)
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.WriteOnly)
    ok = cropped.save(buf, fmt)
    buf.close()
    if not ok:
        raise RuntimeError("Failed to encode cropped image.")
    return bytes(ba)
