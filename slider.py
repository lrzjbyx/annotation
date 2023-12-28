import threading

import cv2
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QSlider, QLineEdit, QComboBox
from PyQt5.uic import loadUi

import utils
# from paddleocr import PaddleOCR, draw_ocr

class slider(QWidget):
    updateSignal = pyqtSignal(bool)
    updateAffiliateSignal = pyqtSignal(bool)
    def __init__(self, item):
        super(slider, self).__init__(None)
        loadUi("./ui/slider.ui", self)
        self.item = item
        self.affiliate = None
        self.setWindowTitle(self.item.name)
        self.horizontalSlider_2.setRange(0, 360)
        self.horizontalSlider_3.setRange(0, 360)
        self.horizontalSlider.setRange(1,500)
        self.lineEdit.setPlaceholderText("请输入标注文本")
        self.comboBox.addItems(self.item.sequence)
        self.comboBox.setCurrentIndex(0)
        # c1.addItems(['item-%s' % i for i in range(10)])


        # QComboBox().addItem()
        # print(self.item.parent.GraphicsTypeDict)

        # self.comboBox_2
        self.comboBox_2.currentIndexChanged.connect(self.setAffiliate)
        # Affiliate


        self.horizontalSlider_2.setValue(self.item.startAngle)
        self.horizontalSlider_3.setValue(self.item.spanAngle)
        self.horizontalSlider.setValue(self.item.lineWidth)
        # self.lineEdit.setText(self.item.text)


        self.horizontalSlider_2.valueChanged.connect(self.startAngle)
        self.horizontalSlider_3.valueChanged.connect(self.spanAngle)
        self.horizontalSlider.valueChanged.connect(self.lineWidth)
        self.lineEdit.textChanged.connect(self.textEdit)
        self.pushButton.clicked.connect(self.recognition)

    def startAngle(self,value):
        self.item.startAngle = value *16
        self.updateSignal.emit(True)


    def _setAffiliate(self,value):
        self.affiliate = value

    def spanAngle(self,value):
        self.item.spanAngle = value *16
        self.updateSignal.emit(True)

    def lineWidth(self,value):
        self.item.lineWidth = value
        self.updateSignal.emit(True)

    def textEdit(self,value):
        self.item.text = value
        self.updateAffiliateSignal.emit(True)


    def updateAffiliate(self):
        self.comboBox_2.clear()
        print(self.item.parent.GraphicsTypeDict)
        roots  = []
        for k,v in self.item.parent.GraphicsTypeDict.items():
            if not v["table_item"]["area"] is None:
                roots.append(k)

        self.comboBox_2.addItems(roots)

        if self.item.affiliate is None:
            self.item.affiliate = self.affiliate
            print(self.item.affiliate)
            if self.affiliate is None:
                return

        if not self.affiliate is None:
            self.comboBox_2.setCurrentIndex(roots.index(self.affiliate))
            self.updateAffiliateSignal.emit(True)



    def setAffiliate(self):
        text = self.comboBox_2.currentText()

        if not text == "":
            self.item.affiliate = text
            self.updateAffiliateSignal.emit(True)


    def recognition(self):
        th = threading.Thread(target=self.fitAlign)
        th.start()


    def fitAlign(self):
        # 将 图片转换成 ndarray
        nd = utils.qQixmapConvertNd( self.item.parent._pixmap)
        item = self.item.label()
        if item["type"] == 2:
            item["la"] = 0
            item["mu"] = 1
        elif item["type"] == 5:
            item["la"] = 1
            item["mu"] = 0
            item["a"] = item["r"]
            item["b"] = item["r"]
        elif item["type"] == 6:
            item["la"] = 1
            item["mu"] = 0
        else:
            return

        image = self.item.parent.parent.align.run(nd, item)
        xx = QPixmap(utils.ndConvertQpixmap(image)).scaled(QSize(235,73),Qt.KeepAspectRatio,Qt.SmoothTransformation)
        self.image_align.setPixmap(xx)

        # cv2.imwrite("1.png",image)

        result = self.item.parent.parent.paddle.ocr(image)

        label_str = ""
        for line in result[0]:
            label_str+=line[1][0]

        self.lineEdit.setText(label_str)

        # print(label_str)