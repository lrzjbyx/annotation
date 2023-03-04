from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.Qt import QDir

from PyQt5 import  QtGui, QtWidgets, QtCore, QtWinExtras
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class treeWidget(QTreeWidget):

    def mouseMoveEvent_xxx(self, e):
        mimeData = QtCore.QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)

        # pixmap = QPixmap()
        # drag.setPixmap(pixmap)

        # drag.setHotSpot(e.pos())

        # QTreeWidget.mouseMoveEvent(self,e)
        drag.exec_(QtCore.Qt.MoveAction)

    def dropEvent(self, e):
        QTreeWidget.dropEvent(self, e)
        self.expandAll()
        e.accept()

    def startDrag(self, supportedActions):
        listsQModelIndex = self.selectedIndexes()
        if listsQModelIndex:
            dataQMimeData = self.model().mimeData(listsQModelIndex)
            if not dataQMimeData:
                return None

            dragQDrag = QDrag(self)
            # custom image here
            dragQDrag.setMimeData(dataQMimeData)

            # combobox = QComboBox()
            # combobox.addItems(['右下文字', '左下文字', '水平文字', '左平文字', '右平文字'])
            # self.dataQMimeData.setItemWidget(dataQMimeData, 2, combobox)
            #
            # line_edit = QLineEdit()
            # line_edit.setReadOnly(True)
            # self.dataQMimeData.setItemWidget(dataQMimeData, 3, line_edit)
            #



            defaultDropAction = QtCore.Qt.IgnoreAction
            if ((supportedActions & QtCore.Qt.CopyAction) and (self.dragDropMode() != QAbstractItemView.InternalMove)):
                defaultDropAction = QtCore.Qt.CopyAction
            dragQDrag.exec_(supportedActions, defaultDropAction)
