# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QMainWindow, QPushButton, QHBoxLayout, QLabel, QWidget, \
    QVBoxLayout, QApplication

class customListWidgetItem(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.iconQLabel = QLabel()
        self.filenameQLabel = QLabel()
        layout.addWidget(self.iconQLabel, 0)
        layout.addWidget(self.filenameQLabel, 1)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)


    def setFilename (self, text):
        self.filenameQLabel.setText(text)

    def setIcon (self, imagePath):
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaledToWidth(16,Qt.SmoothTransformation)
        self.iconQLabel.setPixmap(pixmap)



#
# class QCustomQWidget (QWidget):
#     def __init__ (self, parent = None):
#         super(QCustomQWidget, self).__init__(parent)
#         self.textQVBoxLayout = QVBoxLayout()
#         self.textUpQLabel    = QLabel()
#         self.textDownQLabel  = QLabel()
#         self.textQVBoxLayout.addWidget(self.textUpQLabel)
#         self.textQVBoxLayout.addWidget(self.textDownQLabel)
#         self.allQHBoxLayout  = QHBoxLayout()
#         self.iconQLabel      = QLabel()
#         self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
#         self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
#         self.setLayout(self.allQHBoxLayout)
#         # setStyleSheet
#         # self.textUpQLabel.setStyleSheet('''
#         #     color: rgb(0, 0, 255);
#         # ''')
#         # self.textDownQLabel.setStyleSheet('''
#         #     color: rgb(255, 0, 0);
#         # ''')
#
#     def setTextUp (self, text):
#         self.textUpQLabel.setText(text)
#
#     def setTextDown (self, text):
#         self.textDownQLabel.setText(text)
#
#     def setIcon (self, imagePath):
#         # pass
#         pixmap = QPixmap(imagePath)
#         pixmap = pixmap.scaledToWidth(30,Qt.SmoothTransformation)
#
#         self.iconQLabel.setPixmap(pixmap)
#         # self.iconQLabel.setIcon(QIcon(QPixmap(imagePath)))
#         # self.iconQLabel.setPixmap()

# class exampleQMainWindow (QMainWindow):
#     def __init__ (self):
#         super(exampleQMainWindow, self).__init__()
#         # Create QListWidget
#         self.myQListWidget = QListWidget(self)
#         for index, name, icon in [
#             ('No.1', 'Meyoko',  'res/finish-2.png'),
#             ('No.2', 'Nyaruko', 'res/finish-2.png'),
#             ('No.3', 'Louise',  'res/finish-2.png')]:
#             # Create QCustomQWidget
#             myQCustomQWidget = customListWidgetItem()
#             myQCustomQWidget.setFilename(index)
#             myQCustomQWidget.setIcon(icon)
#             # Create QListWidgetItem
#             myQListWidgetItem = QListWidgetItem(self.myQListWidget)
#             # Set size hint
#             # myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
#             # Add QListWidgetItem into QListWidget
#             self.myQListWidget.addItem(myQListWidgetItem)
#             self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
#         self.setCentralWidget(self.myQListWidget)
#
#         # print(QListWidget().currentIndex().row())
#         # # self.myQListWidget.itemWidget(self.myQListWidget.item(0)).setTextUp("res/finish-2.png")
#         # self.myQListWidget.itemWidget(self.myQListWidget.item(0)).setIcon("res/finish-2.png")
#

# app = QApplication([])
# window = exampleQMainWindow()
# window.show()
# sys.exit(app.exec_())