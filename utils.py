import json

import cv2
import numpy as np
from PyQt5.QtGui import QImage


def loadLabelJson(filename):
    with open(filename,"r",encoding="utf-8") as f:
        content = f.read()
    return json.loads(content)


def qQixmapConvertNd(pixmap):
    qimg = pixmap.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]

    return result


def ndConvertQpixmap(ndimage):
    height, width, depth = ndimage.shape
    ndimage = cv2.cvtColor(ndimage, cv2.COLOR_BGR2RGB)
    qimage = QImage(ndimage.data, width, height, width * depth, QImage.Format_RGB888)

    return qimage
