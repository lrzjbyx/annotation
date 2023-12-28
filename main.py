import json
import os

import numpy as np
from PyQt5.QtCore import QStringListModel, pyqtSignal, QPoint, QRectF, Qt, QPointF, QLineF, QObject, QEvent, \
    QItemSelectionModel, QModelIndex, QSize, QUrl
from PyQt5.QtGui import QPixmap, QBrush, QPen, QPainter, QColor, QPainterPath, QImage, QIcon, QStandardItemModel, \
    QStandardItem, QMouseEvent, QKeySequence, QConicalGradient, QLinearGradient, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QListView, QAbstractItemView, \
    QGraphicsEllipseItem, QGraphicsItem, QGraphicsRectItem, QSlider, QHeaderView, QTreeWidgetItem, QLabel, QHBoxLayout, \
    QComboBox, QLineEdit, QTreeWidget, QTableWidgetItem, QTableWidget, QGraphicsScene, QMenu, QGraphicsView, \
    QListWidgetItem, QShortcut, QAction, QToolButton, QUndoStack
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtCore, QtGui
from pyqt5_plugins.examplebutton import QtWidgets

import align
import scene
from item import *
from linker import linker
from listw import customListWidgetItem
from slider import  slider
import cv2
from paddleocr import PaddleOCR, draw_ocr


from config import configure
from tablew import tableColorWidget, tableGraphicsWidget, tableBasicWidget
from utils import loadLabelJson


class GraphicsRectItem(GraphicsBasicItem):
    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.linker = linker(self)


    def triggerLinkerShow(self):
        self.linker.loadLeftListItem()
        if self.linker.isVisible():
            self.linker.hide()
        else:
            self.linker.show()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.triggerLinkerShow()

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        r, g, b, a = configure["tag"][0]["color"]
        painter.setBrush(QBrush(QColor(r, g, b, a)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():

            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)

    def label(self)->dict:

        affiliateDict = self.linker.affiliate()

        labelData = {}
        labelData["x"] = self.x()
        labelData["y"] = self.y()
        labelData["rect"] =  [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]
        labelData["rotation"] = round(self.angle,3)
        # 类型
        labelData["type"] = PaintType.rectangle.value
        labelData["groups"] = []
        # 未分组的线条标注
        labelData["raws"] = []

        rightTable = self.linker.rightTable
        print(rightTable.rowCount())
        for i in range(rightTable.rowCount()):
            # 获取id  cirlce_1
            id = rightTable.item(i, 0).text()
            # 获取文本
            text = rightTable.item(i, 1).text()
            labelData["raws"].append(self.parent.GraphicsTypeDict[id]["graph_item"].label())

        for k,v in affiliateDict.items():
            d = {}
            d["group"] = k
            d["relationship"] = v["relationship"]
            d["relationship"] = v["relationship"]
            d["links"] = []
            for a in v["affiliate"]:
                d["links"].append({
                    "name":a,
                    "entity":self.parent.GraphicsTypeDict[a]["graph_item"].label()
                })

            labelData["groups"].append(d)
        return labelData


class GraphicsCircleItem(GraphicsBasicItem):
    def __init__(self,*args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.linker = linker(self)

    def triggerLinkerShow(self):
        self.linker.loadLeftListItem()
        if self.linker.isVisible():
            self.linker.hide()
        else:
            self.linker.show()

    def label(self)->dict:

        affiliateDict = self.linker.affiliate()

        labelData = {}
        labelData["x"] = self.x()
        labelData["y"] = self.y()
        labelData["rect"] =  [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]
        labelData["rotation"] = round(self.angle,3)
        # 类型
        labelData["type"] = PaintType.circle.value
        labelData["groups"] = []

        # 未分组的线条标注
        labelData["raws"] = []

        rightTable = self.linker.rightTable
        for i in range(rightTable.rowCount()):
            # 获取id  cirlce_1
            id = rightTable.item(i, 0).text()
            # 获取文本
            text = rightTable.item(i, 1).text()
            labelData["raws"].append(self.parent.GraphicsTypeDict[id]["graph_item"].label())

        for k,v in affiliateDict.items():
            d = {}
            d["group"] = k
            d["relationship"] = v["relationship"]
            d["links"] = []
            for a in v["affiliate"]:
                d["links"].append({
                    "name":a,
                    "entity":self.parent.GraphicsTypeDict[a]["graph_item"].label()
                })

            labelData["groups"].append(d)

        return labelData

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.triggerLinkerShow()

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        r,g,b,a = configure["tag"][1]["color"]
        painter.setBrush(QBrush(QColor(r,g,b,a)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawEllipse(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                if  handle == self.handleTopMiddle or handle == self.handleBottomMiddle :
                    painter.drawEllipse(rect)






    def interactiveResize(self, mousePos):
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        print(rect)
        if self.handleSelected == self.handleTopMiddle:
            fromY = self.mousePressRect.top()
            fromX = self.mousePressRect.left()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toX = fromX + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setTop(toY)
            boundingRect.setLeft(toX)
            rect.setTop(boundingRect.top() + offset)
            rect.setLeft(boundingRect.left() + offset)
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            fromX = self.mousePressRect.right()

            toY = fromY + mousePos.y() - self.mousePressPos.y()
            toX = fromX + mousePos.y() - self.mousePressPos.y()

            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            boundingRect.setRight(toX)
            rect.setBottom(boundingRect.bottom() - offset)
            rect.setRight(boundingRect.right() - offset)

            self.setRect(rect)



        self.updateHandlesPos()


class GraphicsEllipseItem(GraphicsBasicItem):
    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)
        self.linker = linker(self)

    def triggerLinkerShow(self):
        self.linker.loadLeftListItem()
        if self.linker.isVisible():
            self.linker.hide()
        else:
            self.linker.show()

    def label(self)->dict:

        affiliateDict = self.linker.affiliate()

        labelData = {}
        labelData["x"] = self.x()
        labelData["y"] = self.y()
        labelData["rect"] =  [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]
        labelData["rotation"] = round(self.angle,3)
        # 类型
        labelData["type"] = PaintType.ellipse.value
        # 已经分组
        labelData["groups"] = []
        # 未分组的线条标注
        labelData["raws"] = []

        rightTable = self.linker.rightTable
        for i in range(rightTable.rowCount()):
            # 获取id  cirlce_1
            id = rightTable.item(i, 0).text()
            # 获取文本
            text = rightTable.item(i, 1).text()
            labelData["raws"].append(self.parent.GraphicsTypeDict[id]["graph_item"].label())



        for k,v in affiliateDict.items():
            d = {}
            d["group"] = k
            d["relationship"] = v["relationship"]
            d["relationship"] = v["relationship"]



            d["links"] = []
            for a in v["affiliate"]:
                d["links"].append({
                    "name":a,
                    "entity":self.parent.GraphicsTypeDict[a]["graph_item"].label()
                })

            labelData["groups"].append(d)
        return labelData

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.triggerLinkerShow()

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        # painter.setBrush(QBrush(QColor(colorList2intSet(configure["tag"][2]["color"]))))
        # painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        r, g, b, a = configure["tag"][2]["color"]
        painter.setBrush(QBrush(QColor(r, g, b, a)))
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.drawEllipse(self.rect())


        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)


class GraphicsCircleRrcItem(GraphicsCircleItem):

    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)

        self.startAngle = 0
        self.spanAngle = 16*180

        self.lineWidth = 100
        self.text = ""
        self.sequence = configure["sequence"]
        self.affiliate = None
        self.slider = slider(self)
        self.slider.updateSignal.connect(self.repaintGraphics)
        self.slider.updateAffiliateSignal.connect(self.saveRelationship)

    def label(self)->dict:
        labelData = {}
        # x坐标
        labelData["x"] = self.x()
        # y坐标
        labelData["y"] = self.y()
        # 外接矩形
        labelData["rect"] =  [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]
        # 旋转角度
        labelData["rotation"] = round(self.angle,3)
        # 文本
        labelData["text"] = self.text
        # 序列方式
        labelData["sequence"] = self.slider.comboBox.currentText()
        # 类型
        labelData["type"] = PaintType.circle_arc.value
        # 开始角度
        labelData["startAngle"] = self.startAngle
        # 间隔角度
        labelData["spanAngle"] = self.spanAngle
        # 半径
        labelData["r"] = self.rect().width() / 2
        #宽度
        labelData["h"] = self.lineWidth

        return labelData




    def saveRelationship(self):
        self.parent.RelationshipDict[self.name] = {"name": self.affiliate, "text": self.text}

    def repaintGraphics(self):
        self.update()



    def paint(self, painter, option, widget=None):
        print(self.name)
        """
        Paint the node in the graphic view.
        """
        r, g, b, a = configure["tag"][4]["color"]


        #  外围扇形
        outRect = QRectF(self.rect().center().x()-(self.rect().width()+self.lineWidth)/2,self.rect().center().y()-(self.rect().width()+self.lineWidth)/2,
                         self.rect().width()+int(self.lineWidth),self.rect().height()+int(self.lineWidth))

        #  内测扇形
        inRect = QRectF(self.rect().center().x()-(self.rect().width()-self.lineWidth)/2,self.rect().center().y()-(self.rect().width()-self.lineWidth)/2,
                        self.rect().width()-int(self.lineWidth),self.rect().height()-int(self.lineWidth))


        # 绘制圆弧
        path1 = QPainterPath()
        path1.moveTo(self.rect().center().x(),self.rect().center().y())
        path1.arcTo(outRect, self.startAngle/16, (self.spanAngle)/16)
        path1.closeSubpath()

        path2 = QPainterPath()
        path2.moveTo(self.rect().center().x(),self.rect().center().y())
        path2.arcTo(inRect, 0, 360)
        path2.closeSubpath()
        path = path1 - path2
        painter.fillPath(path, QColor(r, g, b, a))





        # 中心弧线
        painter.setPen(QPen(QColor(0, 0, 0), 5,Qt.SolidLine,Qt.SquareCap,Qt.MiterJoin))
        painter.drawArc(self.rect(), self.startAngle, self.spanAngle)



        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if  handle == self.handleTopMiddle or handle == self.handleBottomMiddle :
                painter.drawEllipse(rect)



    def triggerSliderShow(self):
        self.slider.updateAffiliate()
        # self.slider.fitAlign()
        if self.slider.isVisible():
            self.slider.hide()
        else:
            self.slider.show()




    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.triggerSliderShow()

class GraphicsEllipseRrcItem(GraphicsEllipseItem):
    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)

        self.startAngle = 0
        self.spanAngle = 16*180

        self.lineWidth = 100

        self.text = ""

        self.sequence = configure["sequence"]
        self.affiliate = None

        print(self.parent.GraphicsTypeDict)

        self.slider = slider(self)

        self.slider.updateSignal.connect(self.repaintGraphics)
        self.slider.updateAffiliateSignal.connect(self.saveRelationship)

    def label(self) -> dict:
        labelData = {}
        labelData["x"] = self.x()
        labelData["y"] = self.y()
        labelData["rect"] = [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]
        labelData["rotation"] = round(self.angle,3)
        labelData["text"] = self.text
        labelData["type"] = PaintType.ellipse_arc.value
        labelData["sequence"] = self.slider.comboBox.currentText()
        # 开始角度
        labelData["startAngle"] = self.startAngle
        # 间隔角度
        labelData["spanAngle"] = self.spanAngle
        # a 半长轴
        labelData["a"] = self.rect().width() / 2
        # b 半短轴
        labelData["b"] = self.rect().height() / 2
        # 宽度
        labelData["h"] = self.lineWidth



        return labelData

    def saveRelationship(self):
        self.parent.RelationshipDict[self.name] = {"name": self.affiliate, "text": self.text}

    def repaintGraphics(self):
        self.update()

    def triggerSliderShow(self):
        self.slider.updateAffiliate()
        if self.slider.isVisible():
            self.slider.hide()
        else:
            self.slider.show()


    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.triggerSliderShow()



    def paint(self, painter, option, widget=None):
        print(self.name)
        """
        Paint the node in the graphic view.
        """
        r, g, b, a = configure["tag"][5]["color"]


        #  外围扇形
        outRect = QRectF(self.rect().center().x()-(self.rect().width()+self.lineWidth)/2,self.rect().center().y()-(self.rect().height()+self.lineWidth)/2,
                         self.rect().width()+int(self.lineWidth),self.rect().height()+int(self.lineWidth))

        #  内测扇形
        inRect = QRectF(self.rect().center().x()-(self.rect().width()-self.lineWidth)/2,self.rect().center().y()-(self.rect().height()-self.lineWidth)/2,
                        self.rect().width()-int(self.lineWidth),self.rect().height()-int(self.lineWidth))


        # 绘制圆弧
        path1 = QPainterPath()
        path1.moveTo(self.rect().center().x(),self.rect().center().y())
        path1.arcTo(outRect, self.startAngle/16, (self.spanAngle)/16)
        path1.closeSubpath()


        path2 = QPainterPath()
        path2.addEllipse(inRect)
        path2.closeSubpath()
        path = path1 - path2
        painter.fillPath(path, QColor(r, g, b, a))


        # 中间 线条
        painter.setPen(QPen(QColor(0, 0, 0), 5, Qt.SolidLine))
        painter.drawArc(self.rect(), self.startAngle, self.spanAngle)




        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawEllipse(rect)


class GraphicsLineItem(GraphicsBasicItem):
    def __init__(self, *args):
        """
        Initialize the shape.
        """
        super().__init__(*args)

        self.startAngle = 0
        self.spanAngle = 0
        self.lineWidth = 100
        self.text = ""
        self.sequence = configure["sequence"]
        self.affiliate = None

        self.slider = slider(self)

        self.slider.updateSignal.connect(self.repaintGraphics)

        self.slider.updateAffiliateSignal.connect(self.saveRelationship)

    def label(self) -> dict:
        labelData = {}
        labelData["x"] = self.x()
        labelData["y"] = self.y()
        labelData["rect"] = [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]
        labelData["rotation"] = round(self.angle,3)
        labelData["text"] = self.text
        labelData["type"] = PaintType.line.value
        labelData["sequence"] = self.slider.comboBox.currentText()
        # 线条长度
        labelData["l"] = self.rect().width()
        labelData["h"] = self.lineWidth

        return labelData

    def saveRelationship(self):
        self.parent.RelationshipDict[self.name] = {"name": self.affiliate, "text": self.text}


    def repaintGraphics(self):
        self.update()

    def triggerSliderShow(self):
        self.slider.updateAffiliate()
        if self.slider.isVisible():
            self.slider.hide()
        else:
            self.slider.show()

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.triggerSliderShow()





    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        # 两个左侧中心点
        middleLeftPoint = QPoint(self.handles[self.handleMiddleLeft].x()+4,self.handles[self.handleMiddleLeft].y()+4)
        middrightPoint = QPoint(self.handles[self.handleMiddleRight].x()+4, self.handles[self.handleMiddleRight].y()+4)

        # 绘制直线外接区域
        r, g, b, a = configure["tag"][3]["color"]
        print(self.boundingRect())
        painter.setPen(QPen(QColor(r, g, b, a)))
        painter.setBrush(QBrush(QColor(r, g, b, a)))
        rect = QRectF(middleLeftPoint.x(),middleLeftPoint.y()-self.lineWidth/2,self.rect().width(),self.lineWidth)
        painter.drawRect(rect)



        # 绘制中间线
        painter.setPen(QPen(QColor(0, 0, 0), 5, Qt.SolidLine))
        painter.drawLine(middleLeftPoint, middrightPoint)

        # 绘制两个边点
        painter.setBrush(QBrush(QColor(255, 0, 0, 255)))
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                if handle == self.handleMiddleRight or handle == self.handleMiddleLeft:
                    painter.drawEllipse(rect)


class PhotoViewer(QtWidgets.QGraphicsView):
    # photoClicked = pyqtSignal(QPoint)
    paintSignal = pyqtSignal(dict)
    rotationSignal = pyqtSignal(int)
    deleteSignal =  pyqtSignal(bool)
    saveSignal = pyqtSignal(dict)
    fineTuneSignal =  pyqtSignal(bool)
    GraphicsTypeCount = [0,0,0,0,0,0,0]
    # manage graph
    GraphicsTypeDict = {}
    # manage relation
    RelationshipDict = {}
    # manage raws
    RawsDict = {}

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        # self._scene = QtWidgets.QGraphicsScene(self)
        self._scene = scene.PhotoScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._pixmap = QPixmap()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.parent = parent


        #设置右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_click_menu)

        # 设置
        self.paintSignal.connect(self.paintGraphics)
        # 设置旋转
        self.rotationSignal.connect(self.rotation)
        # 设置删除
        self.deleteSignal.connect(self.deleteItem)
        # 父亲的保存
        self.parent.pushButton_16.clicked.connect(self.saveGraphicsItem)
        self.parent.pushButton_16.setIconSize(QSize(24, 24))
        self.parent.pushButton_16.setIcon(QIcon("res/save.png"))
        self.parent.pushButton_16.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)



        QShortcut(QKeySequence(self.tr("Ctrl+S")), self, self.saveGraphicsItem)
        # self.parent.pushButton_16.setShortcut("Alt+s")
        # 微调处理
        self.fineTuneSignal.connect(self.tuneRatationAngle)
        # 设置更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)


    def right_click_menu(self, pos):
        if self.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            print("鼠标点击点位置({0},{1})".format(pos.x(), pos.y()))
            try:
                # 鼠标事件
                event = QMouseEvent(QEvent.MouseButtonRelease,pos,Qt.LeftButton, Qt.LeftButton,Qt.NoModifier)
                # 支持拖拽的鼠标相对位置点
                rpos = self.mapToScene(event.pos()).toPoint()
                print("支持拖拽后的鼠标相对位置点({0},{1})".format(rpos.x(),rpos.y()))
                self._context_menu = QMenu()
                # 圆标注
                self._action_circle_label = self._context_menu.addAction(QIcon("res/circle.png"),u'圆')
                self._action_circle_label.triggered.connect(lambda x:self.paintGraphics({"type": PaintType.circle, "rect": QRectF(rpos.x(),rpos.y(),300,300)}))

                self._action_rect_label = self._context_menu.addAction(QIcon("res/rect.png"),u'矩形')
                self._action_rect_label.triggered.connect(
                    lambda x: self.paintGraphics({"type": PaintType.rectangle,  "rect": QRectF(rpos.x(),rpos.y(),300,150)}))

                self._action_ellipse_label = self._context_menu.addAction(QIcon("res/ellipse.png"),u'椭圆')
                self._action_ellipse_label.triggered.connect(
                    lambda x: self.paintGraphics({"type": PaintType.ellipse, "rect": QRectF(rpos.x(),rpos.y(),300,150)}))

                self._context_menu.addSeparator()

                self._action_line_label = self._context_menu.addAction(QIcon("res/line.png"),u'直线')
                self._action_line_label.triggered.connect(
                    lambda x: self.paintGraphics({"type": PaintType.line, "rect": QRectF(rpos.x(),rpos.y(),300, 10)}))

                self._action_circle_arc_label = self._context_menu.addAction(QIcon("res/circle-arc.png"),u'圆弧')
                self._action_circle_arc_label.triggered.connect(
                    lambda x: self.paintGraphics({"type": PaintType.circle_arc, "rect": QRectF(rpos.x(),rpos.y(),300, 300)}))

                self._action_ellipse_arc_label = self._context_menu.addAction(QIcon("res/ellipse-arc.png"),u'椭圆弧')
                self._action_ellipse_arc_label.triggered.connect(
                    lambda x: self.paintGraphics({"type": PaintType.ellipse_arc, "rect": QRectF(rpos.x(),rpos.y(),300, 150)}))

                self._context_menu.exec_(self.mapToGlobal(pos))

            except Exception as e:
                print(e)


    def deleteItem(self,value):

        table_items_1 = []
        table_items_2 = []
        graph_items = []
        name_item =[]

        for k, v in self.GraphicsTypeDict.items():
            if not v["table_item"]["area"] is None:
                table_items_1.append(v["table_item"])
            else:
                table_items_2.append(v["table_item"])

            graph_items.append(v["graph_item"])
            name_item.append(k)

        if value :
            items = self._scene.selectedItems()
            # root = self.parent.widget_6.invisibleRootItem()

            for item in items:
                index = graph_items.index(item)
                remove_table_item = self.GraphicsTypeDict[name_item[index]]["table_item"]
                if not remove_table_item["area"] is None:
                    self.parent.tableWidget_6.removeRow(remove_table_item["area"].row())
                elif not remove_table_item["text"] is None:
                    print(remove_table_item["text"].row())
                    self.parent.tableWidget_7.removeRow(remove_table_item["text"].row())
                self.GraphicsTypeDict.pop(name_item[index])
                self._scene.removeItem(item)

                if name_item[index] in self.RelationshipDict.keys():
                    del self.RelationshipDict[name_item[index]]




    def rotation(self,value,item=None):
        if item is None:
            items = self._scene.selectedItems()
            for item in items:
                # void QGraphicsItem::setTransformOriginPoint(qreal x, qreal y)
                # print()
                item.setTransformOriginPoint(item.boundingRect().center().x(),item.boundingRect().center().y())
                item.setRotation(value)
                item.angle = value
                # item.update()
        else:
            item.setTransformOriginPoint(item.boundingRect().center().x(), item.boundingRect().center().y())
            item.setRotation(value)
            item.angle = value
            # item.update()




    def tuneRatationAngle(self,value):
        if value:
            self.enlargeRatationAngle()
        else:
            self.minishRatationAngle()


    def enlargeRatationAngle(self):
        items = self._scene.selectedItems()

        for item in items:
            # void QGraphicsItem::setTransformOriginPoint(qreal x, qreal y)
            # print()
            item.setTransformOriginPoint(item.boundingRect().center().x(), item.boundingRect().center().y())
            angle = item.angle
            item.setRotation(angle + 0.1)
            item.angle = angle + 0.1

    def minishRatationAngle(self):
        items = self._scene.selectedItems()

        for item in items:
            item.setTransformOriginPoint(item.boundingRect().center().x(), item.boundingRect().center().y())
            angle = item.angle
            item.setRotation(angle - 0.1)
            item.angle = angle - 0.1


    def labelPaintGraphics(self,label_data):
        for label in label_data:
            region_label_name = self.paintGraphics({"type":label["type"],"rect":QRectF(label["rect"][0]+label["x"],label["rect"][1]+label["y"],label["rect"][2],label["rect"][3])})
            region_item = self.GraphicsTypeDict[region_label_name]["graph_item"]
            # 旋转图片
            self.rotation(label["rotation"],region_item)

            if "groups" not in label.keys():
                arc_item = self.GraphicsTypeDict[region_label_name]["graph_item"]
                # 设置文本
                arc_item.text = label["text"]
                # 设置序列
                arc_item.sequence = label["sequence"]

                if not label["type"] == PaintType.line.value:
                    # 设置弧度开始结束
                    arc_item.startAngle = label["startAngle"]
                    arc_item.spanAngle = label["spanAngle"]

                arc_item.lineWidth = label["h"]
                # 设置slider 文字
                arc_item.slider.lineEdit.setText(label["text"])
                # 设置序列
                arc_item.slider.comboBox.setCurrentIndex(configure["sequence"].index(label["sequence"]))
                continue



            # 分组还原
            for group in label["groups"]:
                # 添加组
                group_data = {"relationship":group["relationship"],"links":[]}
                # region_item.linker.leftList
                for link in group["links"]:
                    arc_item_name =  self.paintGraphics({"type":link["entity"]["type"],"rect":QRectF(link["entity"]["rect"][0]+link["entity"]["x"],link["entity"]["rect"][1]+link["entity"]["y"],link["entity"]["rect"][2],link["entity"]["rect"][3])})
                    arc_item = self.GraphicsTypeDict[arc_item_name]["graph_item"]
                    group_data["links"].append({"name":arc_item_name,"text":link["entity"]["text"]})
                    # 旋转
                    self.rotation(link["entity"]["rotation"], arc_item)
                    # 设置隶属于
                    # arc_item.affiliate = region_label_name
                    arc_item.slider._setAffiliate(region_label_name)
                    # 设置文本
                    arc_item.text = link["entity"]["text"]
                    # 设置序列
                    arc_item.sequence = link["entity"]["sequence"]
                    if not link["entity"]["type"] == PaintType.line.value:
                        # 设置弧度开始结束
                        arc_item.startAngle = link["entity"]["startAngle"]
                        arc_item.spanAngle = link["entity"]["spanAngle"]
                    # 设置宽度
                    arc_item.lineWidth = link["entity"]["h"]

                    #### 设置slider
                    # 设置slider 文字
                    arc_item.slider.lineEdit.setText(link["entity"]["text"])
                    # 关系设置
                    self.RelationshipDict[arc_item_name] = {"name":region_label_name,"text":link["entity"]["text"]}
                    print(self.RelationshipDict)
                    # 设置序列
                    arc_item.slider.comboBox.setCurrentIndex(configure["sequence"].index(link["entity"]["sequence"]))

                region_item.linker.addGroup(group_data)

                # 保存未分组的数据
                # for raw in group["raws"]:
                #     pass
                    # arc_item_name = self.paintGraphics({"type": raw["type"],
                    #                                     "rect": QRectF(raw["rect"][0] + raw["x"],
                    #                                                    raw["rect"][1] + raw["y"],
                    #                                                    raw["rect"][2],
                    #                                                    raw["rect"][3])})
                    # arc_item = self.GraphicsTypeDict[arc_item_name]["graph_item"]
                    # group_data["links"].append({"name": arc_item_name, "text": raw["text"]})




        for k,v in self.RelationshipDict.items():
            self.GraphicsTypeDict[k]["graph_item"].slider.updateAffiliate()



        print(self.RelationshipDict)








    def paintGraphics(self,data):

        if data["type"] == PaintType.circle or data["type"] == PaintType.circle.value:
            name = "circle-{0}".format(self.GraphicsTypeCount[0])
            # item = GraphicsCircleItem(self, name, data["rect"].x(), data["rect"].y(),300,300)
            item = GraphicsCircleItem(self,name,data["rect"].x(), data["rect"].y(), data["rect"].width(), data["rect"].height())
            self._scene.addItem(item)
            tt = {}
            tt["graph_item"] = item
            tt["table_item"] = {
                "area":None,"text":None
            }
            self.GraphicsTypeDict[name] = tt
            self.parent.saveLabelItem(name,0)
            self.GraphicsTypeCount[0] += 1
        elif data["type"]  == PaintType.rectangle  or data["type"] == PaintType.rectangle.value:
            name = "rectangle-{0}".format(self.GraphicsTypeCount[1])
            # item = GraphicsRectItem(self,name,data["point"].x(), data["point"].y(), 300, 150)
            item = GraphicsRectItem(self,name,data["rect"].x(), data["rect"].y(), data["rect"].width(), data["rect"].height())
            self._scene.addItem(item)
            tt = {}
            tt["graph_item"] = item
            tt["table_item"] = {
                "area": None, "text": None
            }
            self.GraphicsTypeDict[name] = tt
            self.parent.saveLabelItem(name,0)
            self.GraphicsTypeCount[1] += 1
        elif data["type"]  == PaintType.ellipse  or data["type"] == PaintType.ellipse.value:
            name = "ellipse-{0}".format(self.GraphicsTypeCount[2])
            # item = GraphicsEllipseItem(self,name,data["point"].x(), data["point"].y(), 300, 150)
            item = GraphicsEllipseItem(self,name,data["rect"].x(), data["rect"].y(), data["rect"].width(), data["rect"].height())
            self._scene.addItem(item)
            tt = {}
            tt["graph_item"] = item
            tt["table_item"] = {
                "area": None, "text": None
            }
            self.GraphicsTypeDict[name] = tt
            self.parent.saveLabelItem(name,0)
            self.GraphicsTypeCount[2] += 1

        elif data["type"]  == PaintType.line or data["type"] == PaintType.line.value:
            name = "line-{0}".format(self.GraphicsTypeCount[3])
            # item = GraphicsLineItem(self,name,data["point"].x(), data["point"].y(), 300, 10)
            item = GraphicsLineItem(self,name,data["rect"].x(), data["rect"].y(), data["rect"].width(), data["rect"].height())
            self._scene.addItem(item)
            tt = {}
            tt["graph_item"] = item
            tt["table_item"] = {
                "area": None, "text": None
            }
            self.GraphicsTypeDict[name] = tt
            self.parent.saveLabelItem(name,1)
            self.GraphicsTypeCount[3] += 1

        elif data["type"]  == PaintType.circle_arc or data["type"] == PaintType.circle_arc.value:
            name = "circle_arc-{0}".format(self.GraphicsTypeCount[4])
            # item = GraphicsCircleRrcItem(self,name,data["point"].x(), data["point"].y(), 300, 300)
            item = GraphicsCircleRrcItem(self,name,data["rect"].x(), data["rect"].y(), data["rect"].width(), data["rect"].height())
            self._scene.addItem(item)
            tt = {}
            tt["graph_item"] = item
            tt["table_item"] = {
                "area": None, "text": None
            }
            self.GraphicsTypeDict[name] = tt
            self.parent.saveLabelItem(name,1)
            self.GraphicsTypeCount[4] += 1
        elif data["type"]  == PaintType.ellipse_arc  or data["type"] == PaintType.ellipse_arc.value:
            name = "ellipse_arc-{0}".format(self.GraphicsTypeCount[5])
            # item = GraphicsEllipseRrcItem(self,name,data["point"].x(), data["point"].y(), 300, 150)
            item = GraphicsEllipseRrcItem(self,name,data["rect"].x(), data["rect"].y(), data["rect"].width(), data["rect"].height())
            self._scene.addItem(item)
            tt = {}
            tt["graph_item"] = item
            tt["table_item"] = {
                "area": None, "text": None
            }
            self.GraphicsTypeDict[name] = tt
            self.parent.saveLabelItem(name,1)
            self.GraphicsTypeCount[5] += 1


        return name




    def saveGraphicsItem(self):
        print(self.RelationshipDict)
        print(self.GraphicsTypeDict)
        # 获取全部矩形框
        entitys = {}
        for k,v in self.RelationshipDict.items():
            if not v["name"] in entitys.keys():
                entitys[v["name"]] = []

            entitys[v["name"]].append(k)

        # 返回结果
        result = {"image": {
            "filename": self.parent.current_filename,
            "width": self.parent.current_pixmap.width(),
            "height": self.parent.current_pixmap.height()
        }, "label": []}

        for k,v in entitys.items():
            if k is None:
                for ii in v:
                    result["label"].append(self.GraphicsTypeDict[ii]["graph_item"].label())
                continue

            result["label"].append(self.GraphicsTypeDict[k]["graph_item"].label())


        tt = []
        for k,v in entitys.items():
            tt.append(k)
            tt.extend(v)

        for t in [k  for k in  self.GraphicsTypeDict.keys()  if k not in tt ]:
            result["label"].append(self.GraphicsTypeDict[t]["graph_item"].label())

        filename = os.path.join(self.parent.output_directory,"{0}.json".format(os.path.basename(self.parent.filenames[self.parent.listWidget.currentIndex().row()]).split ('.') [ 0 ]))
        print(filename)
        print(result)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))

        # 更新图标标识
        row = self.parent.listWidget.currentIndex().row()
        item = self.parent.listWidget.item(row)
        self.parent.listWidget.itemWidget(item).setIcon("res/finish-3.png")




    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor*1, factor*1)
                # self.scale(factor*0.8, factor*0.5)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            self._pixmap = pixmap
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0


    # def mousePressEvent(self, event):
    #     if self._photo.isUnderMouse():
    #         self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
    #     super(PhotoViewer, self).mousePressEvent(event)


class AnnotationWindow(QWidget):

    def __init__(self, parent=None):
        super(AnnotationWindow, self).__init__(parent)
        loadUi("./ui/main.ui", self)
        # loadUi("./ui/main_en.ui", self)


        # align
        self.align = align.Align(configure["align_height"],configure["align_width"])
        # ocr
        self.paddle = PaddleOCR(use_angle_cls=True, lang="ch",cls_model_dir=configure["cls_model_dir"],det_model_dir=configure["det_model_dir"],rec_model_dir=configure["rec_model_dir"])
        # self.paddle = PaddleOCR(use_angle_cls=True, lang="ch")

        # input directory
        self.input_directory = os.path.abspath(os.curdir)
        self.output_directory = os.path.abspath(os.curdir)

        # 设置标题
        self.setWindowTitle("数据标注")
        # 设置图标
        self.setWindowIcon(QIcon("res/icon.png"))

        # 文件名称
        self.filenames = None
        # 当前文件名称
        self.current_filename = None
        # 当前图片
        self.current_pixmap =  None

        # load directory
        self.pushButton.clicked.connect(self.changeInputDirectory)
        self.pushButton.setIconSize(QSize(24, 24))
        self.pushButton.setIcon(QIcon("res/opendirectory.png"))
        self.pushButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)



        self.pushButton_11.clicked.connect(self.changeOutputDirectory)
        self.pushButton_11.setIconSize(QSize(24, 24))
        self.pushButton_11.setIcon(QIcon("res/outputdirectory.png"))
        self.pushButton_11.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)



        # 设置视图
        self.viewer = PhotoViewer(self)
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        self.widget_3.setLayout(VBlayout)
        # self.viewer.photoClicked.connect(self.photoClicked)



        # 设置不可编辑
        self.listWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置点击改变视图
        self.listWidget.clicked.connect(self.changeView)
        # 设置删除
        self.pushButton_15.clicked.connect(self.deleteSelectedItem)
        self.pushButton_15.setIconSize(QSize(24, 24))
        self.pushButton_15.setIcon(QIcon("res/delete.png"))
        self.pushButton_15.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


        # 设置上一页
        self.pushButton_9.clicked.connect(self.downPage)
        self.pushButton_9.setIconSize(QSize(24, 24))
        self.pushButton_9.setIcon(QIcon("res/up.png"))
        self.pushButton_9.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


        # 设置下一页
        self.pushButton_12.clicked.connect(self.upPage)
        self.pushButton_12.setIconSize(QSize(24, 24))
        self.pushButton_12.setIcon(QIcon("res/down.png"))
        self.pushButton_12.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 绘制圆
        self.pushButton_8.clicked.connect(self.paintCircle)
        self.pushButton_8.setIconSize(QSize(24, 24))
        self.pushButton_8.setIcon(QIcon("res/circle.png"))
        self.pushButton_8.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 绘制矩形
        self.pushButton_6.clicked.connect(self.paintRectangle)
        self.pushButton_6.setIconSize(QSize(24, 24))
        self.pushButton_6.setIcon(QIcon("res/rect.png"))
        self.pushButton_6.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)



        # 撤销
        self.pushButton_2.clicked.connect(self.undo)
        self.pushButton_2.setIconSize(QSize(24, 24))
        self.pushButton_2.setIcon(QIcon("res/undo.png"))
        self.pushButton_2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.pushButton_2.setShortcut(QKeySequence.Undo)

        # 反撤销
        self.pushButton_3.clicked.connect(self.redo)
        self.pushButton_3.setIconSize(QSize(24, 24))
        self.pushButton_3.setIcon(QIcon("res/anti-undo.png"))
        self.pushButton_3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.pushButton_3.setShortcut(QKeySequence.Redo)

        # help
        self.pushButton_18.clicked.connect(lambda x:QDesktopServices.openUrl(QUrl("https://github.com/lrzjbyx/annotation")))
        self.pushButton_18.setIconSize(QSize(24, 24))
        self.pushButton_18.setIcon(QIcon("res/help.png"))
        self.pushButton_18.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # pushButton_10

        # segment anything
        self.pushButton_20.clicked.connect(lambda x:print(x))
        self.pushButton_20.setIconSize(QSize(24, 24))
        self.pushButton_20.setIcon(QIcon("res/anything.png"))
        self.pushButton_20.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 绘制椭圆
        self.pushButton_7.clicked.connect(self.paintEllipse)
        self.pushButton_7.setIconSize(QSize(24, 24))
        self.pushButton_7.setIcon(QIcon("res/ellipse.png"))
        self.pushButton_7.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 绘制直线
        self.pushButton_5.clicked.connect(self.paintLine)
        self.pushButton_5.setIconSize(QSize(24, 24))
        self.pushButton_5.setIcon(QIcon("res/line.png"))
        self.pushButton_5.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


        # 绘制圆弧
        self.pushButton_10.clicked.connect(self.paintCircleArc)
        self.pushButton_10.setIconSize(QSize(24, 24))
        self.pushButton_10.setIcon(QIcon("res/circle-arc.png"))
        self.pushButton_10.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 绘制椭圆弧
        self.pushButton_17.clicked.connect(self.paintEllipseArc)
        self.pushButton_17.setIconSize(QSize(24, 24))
        self.pushButton_17.setIcon(QIcon("res/ellipse-arc.png"))
        self.pushButton_17.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


        # 设置旋转条
        self.verticalSlider.setRange(0, 360)
        self.verticalSlider.valueChanged.connect(self.ratationChange)

        self.pushButton_13.clicked.connect(self.enlargeRatationAngleEmit)
        self.pushButton_13.setIconSize(QSize(24, 24))
        self.pushButton_13.setIcon(QIcon("res/rotation_left.png"))
        self.pushButton_13.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.pushButton_14.clicked.connect(self.minishRatationAngleEmit)
        self.pushButton_14.setIconSize(QSize(24, 24))
        self.pushButton_14.setIcon(QIcon("res/rotation_right.png"))
        self.pushButton_14.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)


        # 保存
        # self.viewer.saveSignal.connect(self.saveGraphicsItem)


        # 标注列表
        # 区域标注
        self.tableWidget_6 = tableGraphicsWidget(header=["区域标注"],parent=self)
        tableLayout_6 =  QHBoxLayout()
        tableLayout_6.addWidget(self.tableWidget_6)
        tableLayout_6.setContentsMargins(0,0,0,0)
        self.widget_6.setLayout(tableLayout_6)
        # 允许打开上下文菜单
        self.tableWidget_6.setContextMenuPolicy(Qt.CustomContextMenu)
        # 绑定事件
        self.tableWidget_6.customContextMenuRequested.connect(self.areaMenu)

        # 实例标注
        self.tableWidget_7 = tableGraphicsWidget(header=["实例标注"],parent=self)
        tableLayout_7 =  QHBoxLayout()
        tableLayout_7.addWidget(self.tableWidget_7)
        tableLayout_7.setContentsMargins(0,0,0,0)
        self.widget_7.setLayout(tableLayout_7)
        # 允许打开上下文菜单
        self.tableWidget_7.setContextMenuPolicy(Qt.CustomContextMenu)
        # 绑定事件
        self.tableWidget_7.customContextMenuRequested.connect(self.arcMenu)

        # 标签样式
        self.tableWidget_5 = tableColorWidget(header=["标签", "颜色"],parent=self)
        tableLayout =  QHBoxLayout()
        tableLayout.addWidget(self.tableWidget_5)
        tableLayout.setContentsMargins(0,0,0,0)
        self.widget_5.setLayout(tableLayout)
        self.tableWidget_5.initRow()




        # 文本读取顺序
        self.tableWidget_8 = tableBasicWidget(header=["文本顺序s"])
        tableLayout_8 =  QHBoxLayout()
        tableLayout_8.addWidget(self.tableWidget_8)
        tableLayout_8.setContentsMargins(0,0,0,0)
        self.widget_8.setLayout(tableLayout_8)


        # 文本读取顺序
        self.tableWidget_9 = tableBasicWidget(header=["文本关联"])
        tableLayout_9 =  QHBoxLayout()
        tableLayout_9.addWidget(self.tableWidget_9)
        tableLayout_9.setContentsMargins(0,0,0,0)
        self.widget_9.setLayout(tableLayout_9)



        # model = QStandardItemModel()
        # self.listView.setModel(model)
        # entries = ["从左到右","从左上到左下","从右上到右下","从左上到右上","左垂直右换行"]
        #
        # for i in entries:
        #     item = QStandardItem(i)
        #     model.appendRow(item)
        #

        self.tableWidget_8.setRowCount(len(configure["sequence"]))
        for i ,v in enumerate(configure["sequence"]):
            self.tableWidget_8.setItem(i, 0, QTableWidgetItem(str(v)))


        # entries = ["从左到右", "从左上到左下", "从右上到右下", "从左上到右上", "左垂直右换行"]
        self.tableWidget_9.setRowCount(len(configure["linked"]))
        for i ,v in enumerate(configure["linked"]):
            self.tableWidget_9.setItem(i, 0, QTableWidgetItem(str(v)))

        # 重置
        self.pushButton_4.clicked.connect(self.reset)
        self.pushButton_4.setIconSize(QSize(24, 24))
        self.pushButton_4.setIcon(QIcon("res/reset.png"))
        self.pushButton_4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 微调
        QShortcut(QKeySequence(self.tr("1")), self, self.enlargeRatationAngleEmit)
        QShortcut(QKeySequence(self.tr("2")), self, self.minishRatationAngleEmit)


        self.undoStack = QUndoStack()
        self.viewer._scene.itemChanged.connect(self.onItemMoved)
        self.viewer._scene.addItemSignal.connect(self.onAddItem)
        self.show()


    #
    def onAddItem(self,item):
        self.undoStack.push(scene.AddCommand(self.viewer._scene, item))
        # pass

    def onItemMoved(self, item, points):
        self.undoStack.push(scene.ChangeCommand(item, points))
        # pass

    def undo(self):
        self.undoStack.undo()

    def redo(self):
        self.undoStack.redo()


    def areaMenu(self, pos):
        print(pos)

        if len(self.tableWidget_6.selectionModel().selection().indexes()) >2:
            return

        # 获取点击行号
        for i in self.tableWidget_6.selectionModel().selection().indexes():
            rowNum = i.row()

        menu = QMenu()
        item1 = menu.addAction(QIcon("res/send_forward.png"),u"上移")
        item2 = menu.addAction(QIcon("res/bring_forward.png"),u"下移")
        item3 = menu.addAction(QIcon("res/lock.png"),u'锁定')
        item4 = menu.addAction(QIcon("res/key.png"),u'解锁')


        # 转换坐标系
        screenPos = self.tableWidget_6.mapToGlobal(pos)
        print(screenPos)
        # xuzhong
        id = self.tableWidget_6.item(rowNum, 0).text()
        graph_item = self.viewer.GraphicsTypeDict[id]["graph_item"]

        # 被阻塞
        action = menu.exec(screenPos)
        if action == item1:
            graph_item.setZValue(graph_item.zValue()+1)
        elif action == item2:
            graph_item.setZValue(graph_item.zValue()-1)
        elif action == item3:
            #获取id  cirlce_1
            self.unlock(graph_item)

        elif action == item4:
            # 获取id  cirlce_1
            self.lock(graph_item)
        else:
            return

    def lock(self,item):
        item.setEnabled(True)

    def unlock(self,item):
        item.setEnabled(False)


    def arcMenu(self,pos):
        print(pos)

        if len(self.tableWidget_7.selectionModel().selection().indexes()) > 2:
            return

        # 获取点击行号
        for i in self.tableWidget_7.selectionModel().selection().indexes():
            rowNum = i.row()

        menu = QMenu()
        item1 = menu.addAction(QIcon("res/send_forward.png"),u"上移")
        item2 = menu.addAction(QIcon("res/bring_forward.png"),u"下移")
        item3 = menu.addAction(QIcon("res/lock.png"),u'锁定')
        item4 = menu.addAction(QIcon("res/key.png"),u'解锁')

        # 转换坐标系
        screenPos = self.tableWidget_7.mapToGlobal(pos)
        print(screenPos)

        # xuzhong
        id = self.tableWidget_7.item(rowNum, 0).text()
        graph_item = self.viewer.GraphicsTypeDict[id]["graph_item"]

        # 被阻塞
        action = menu.exec(screenPos)
        if action == item1:
            graph_item.setZValue(graph_item.zValue()+1)
        elif action == item2:
            graph_item.setZValue(graph_item.zValue()-1)
        elif action == item3:
            # 获取id  cirlce_1
            self.unlock(graph_item)
        elif action == item4:
            # 获取id  cirlce_1
            self.lock(graph_item)
        else:
            return


    def reset(self):
        print(self.viewer.GraphicsTypeDict)

        for k,v in self.viewer.GraphicsTypeDict.items():
            self.viewer._scene.removeItem(v["graph_item"])

        self.viewer.GraphicsTypeDict = {}

        self.tableWidget_6.setRowCount(0)
        self.tableWidget_7.setRowCount(0)

        print(self.viewer.RelationshipDict)
        self.viewer.RelationshipDict = {}
        print(self.viewer.GraphicsTypeCount)
        self.viewer.GraphicsTypeCount = [0, 0, 0, 0, 0, 0, 0]



    def enlargeRatationAngleEmit(self):
        self.viewer.fineTuneSignal.emit(True)

    def minishRatationAngleEmit(self):
        self.viewer.fineTuneSignal.emit(False)


    def saveLabelItem(self,value,type):

        if type==0:
            row = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row)
            item = QTableWidgetItem(str(value))
            self.tableWidget_6.setItem(row, 0, item)
            self.viewer.GraphicsTypeDict[value]["table_item"]["area"] = item
        elif type==1:
            row = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row)
            item = QTableWidgetItem(str(value))
            self.tableWidget_7.setItem(row, 0, item)
            self.viewer.GraphicsTypeDict[value]["table_item"]["text"] = item

    def deleteSelectedItem(self):
        self.viewer.deleteSignal.emit(True)


    def ratationChange(self,value):
        self.viewer.rotationSignal.emit(value)


    def paintCircle(self):
        self.viewer.paintSignal.emit({"type":PaintType.circle,"rect":QRectF(0,0,300,300)})


    def paintRectangle(self):
        self.viewer.paintSignal.emit({"type": PaintType.rectangle, "rect":QRectF(0,0,300, 150)})


    def paintEllipse(self):
        self.viewer.paintSignal.emit({"type": PaintType.ellipse,"rect":QRectF(0,0,300, 150)})

    def paintLine(self):
        self.viewer.paintSignal.emit({"type": PaintType.line, "rect": QRectF(0,0,300, 10)})

    def paintCircleArc(self):
        self.viewer.paintSignal.emit({"type": PaintType.circle_arc, "rect": QRectF(0,0,300, 300)})

    def paintEllipseArc(self):
        self.viewer.paintSignal.emit({"type": PaintType.ellipse_arc, "rect": QRectF(0,0,300, 150)})






    def changeView(self):
        print(self.listWidget.currentIndex().row())
        self.reset()
        # self.listWidget.setCurrentIndex(self.listWidget.currentIndex().row())
        self.current_filename = self.filenames[self.listWidget.currentIndex().row()]
        self.setWindowTitle("数据标注--[{0}...]--[{1}/{2}]".format(self.current_filename,self.listWidget.currentIndex().row()+1,len(self.filenames)))
        self.current_pixmap = QPixmap(os.path.join(self.input_directory, self.current_filename))
        self.viewer.setPhoto(self.current_pixmap)
        self.undoStack.clear()
        self.viewer.toggleDragMode()
        jsonFileName = os.path.join(self.output_directory,"{0}.json".format(self.current_filename.split(".")[0]))
        if os.path.exists(jsonFileName):
            labelData =  loadLabelJson(jsonFileName)
            self.viewer.labelPaintGraphics(labelData["label"])

    def downPage(self):

        row = self.listWidget.currentIndex().row()
        if row-1 >= 0:
            row = row- 1

        # self.listWidget.setCurrentIndex(self.listWidget.model().index(row))
        self.listWidget.setCurrentIndex(self.listWidget.model().index(row,0))
        self.reset()
        self.current_filename = self.filenames[self.listWidget.currentIndex().row()]
        self.setWindowTitle("数据标注--[{0}...]--[{1}/{2}]".format(self.current_filename,self.listWidget.currentIndex().row()+1,len(self.filenames)))
        self.current_pixmap = QPixmap(os.path.join(self.input_directory, self.current_filename))
        self.viewer.setPhoto(self.current_pixmap)
        self.undoStack.clear()
        self.viewer.toggleDragMode()
        jsonFileName = os.path.join(self.output_directory,"{0}.json".format(self.current_filename.split(".")[0]))
        if os.path.exists(jsonFileName):
            labelData =  loadLabelJson(jsonFileName)
            self.viewer.labelPaintGraphics(labelData["label"])



    def upPage(self):

        row = self.listWidget.currentIndex().row()
        if row+1 < len(self.filenames):
            row = row + 1

        self.listWidget.setCurrentIndex(self.listWidget.model().index(row,0))
        self.reset()
        self.current_filename = self.filenames[self.listWidget.currentIndex().row()]
        self.setWindowTitle("数据标注--[{0}...]--[{1}/{2}]".format(self.current_filename,self.listWidget.currentIndex().row()+1,len(self.filenames)))
        print(self.current_filename )
        self.current_pixmap = QPixmap(os.path.join(self.input_directory, self.current_filename))
        self.viewer.setPhoto(self.current_pixmap)
        self.undoStack.clear()
        self.viewer.toggleDragMode()
        jsonFileName = os.path.join(self.output_directory,"{0}.json".format(self.current_filename.split(".")[0]))
        if os.path.exists(jsonFileName):
            labelData =  loadLabelJson(jsonFileName)
            self.viewer.labelPaintGraphics(labelData["label"])
        # self.reset()




    def changeInputDirectory(self):
        self.input_directory = QtWidgets.QFileDialog.getExistingDirectory(self, "输入目录", os.path.abspath(os.curdir))
        # self.input_directory=r"D:\Code\Python\annotation\pic"

        self.output_directory = self.input_directory
        filenames = os.listdir(self.input_directory)
        # 支持的文件后缀
        filenames = [i for i in filenames if os.path.basename(i).split(".")[1] in configure["image_format"]]

        self.filenames = filenames
        self.current_filename = filenames[0]
        self.setWindowTitle("数据标注--[{0}...]--[{1}/{2}]".format(self.current_filename,self.listWidget.currentIndex().row()+1,len(self.filenames)))




        for i ,entity in enumerate(filenames):
            widget = customListWidgetItem()
            widget.setFilename(entity)
            if os.path.exists(os.path.join(self.output_directory,"{0}.json".format(entity.split(".")[0]))):
                widget.setIcon("res/finish-3.png")
            else:
                widget.setIcon("res/pending-2.png")

            listwidgetitem = QListWidgetItem(self.listWidget)
            self.listWidget.addItem(listwidgetitem)
            self.listWidget.setItemWidget(listwidgetitem, widget)



        if len(filenames) > 0:
            print(os.path.join(self.input_directory ,filenames[0]))
            self.listWidget.setCurrentIndex(self.listWidget.model().index(0,0))
            # self.listWidget.selectionModel().select(self.listWidget.model().index(0,0),QItemSelectionModel.Select)
            self.reset()
            self.current_pixmap = QPixmap(os.path.join(self.input_directory, self.current_filename))
            self.viewer.setPhoto(self.current_pixmap)
            self.undoStack.clear()
            self.viewer.toggleDragMode()

            jsonFileName = os.path.join(self.output_directory, "{0}.json".format(self.current_filename.split(".")[0]))
            if os.path.exists(jsonFileName):
                labelData = loadLabelJson(jsonFileName)
                self.viewer.labelPaintGraphics(labelData["label"])


    def changeOutputDirectory(self):
        self.output_directory = QtWidgets.QFileDialog.getExistingDirectory(self, "输出目录", os.path.abspath(os.curdir))



if __name__ == '__main__':
    app = QApplication([])
    win = AnnotationWindow()
    app.exec_()