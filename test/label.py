# from enum import Enum
#
# from PyQt5.QtCore import QSize, Qt
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtWidgets import QWidget, QApplication, QListWidget, QAbstractItemView, QHBoxLayout, QListWidgetItem, QMenu, \
#     QVBoxLayout, QLabel, QPushButton, QLineEdit
# from PyQt5.uic import loadUi
#
#
# class Type(Enum):
#     left = 0
#     right = 1
#
# class customListWidget(QListWidget):
#     def __init__(self, type ,parent=None):
#         super(customListWidget, self).__init__(None)
#         self.parent = parent
#         self.setIconSize(QSize(124, 124))
#         self.setDragDropMode(QAbstractItemView.DragDrop)
#         self.setDefaultDropAction(Qt.MoveAction)
#         self.setSelectionMode(QAbstractItemView.ExtendedSelection)
#         self.setAcceptDrops(True)
#         self.model().rowsInserted.connect(self.handleRowsInserted, Qt.QueuedConnection)
#
#         self.type = type
#
#         # 右键菜单
#         if self.type == Type.left :
#             self.setContextMenuPolicy(Qt.CustomContextMenu)
#             self.customContextMenuRequested.connect(self.left_click_menu)
#
#
#     def handleRowsInserted(self, parent, first, last):
#         for index in range(first, last + 1):
#             item = self.item(index)
#             print("customListWidget-{0}".format(self))
#
#
#             # print(parent.parent().parent())
#             # count = self.itemWidget(item).widget.count()
#             #
#             # print(count)
#
#             # if _item.widget
#
#
#             if item is not None and self.itemWidget(item) is None:
#                 index, name, icon = item.data(Qt.UserRole)
#                 widget = customWidgetItem(self.type,self)
#                 widget.setTextUp(index)
#                 widget.setTextDown(name)
#                 widget.setIcon(icon)
#                 item.setSizeHint(widget.sizeHint())
#                 self.setItemWidget(item, widget)
#
#
#
#     def left_click_menu(self,pos):
#         try:
#             item: QListWidgetItem = self.itemAt(pos)
#             self._context_menu = QMenu()
#
#             # 没有选中节点
#             if item is None:
#                 pass
#             else:
#                 # 增加子Group
#                 self._action_add_group = self._context_menu.addAction(u'设置保存模式')
#                 self._action_add_group.triggered.connect(lambda x: self.setItemSaveModel(item))
#
#                 self._context_menu.addSeparator()
#
#                 # 删除子节点
#                 self._action_child_del = self._context_menu.addAction(u'删除key')
#                 self._action_child_del.triggered.connect(lambda x: print(x))
#
#
#                 self._context_menu.addSeparator()
#
#
#             self._context_menu.exec_(self.mapToGlobal(pos))
#         except Exception as e:
#             print(e)
#
#     def setItemSaveModel(self,item):
#
#         if self.type == Type.left:
#
#             layout = self.parent.widget_2.layout()
#             if not layout is None:
#                 for i in reversed(range(layout.count())):
#                     layout.itemAt(i).widget().setParent(None)
#
#             _, name, _ = item.data(Qt.UserRole)
#
#             self.parent.saveItemName = name
#
#             item = self.itemWidget(item)
#             # self.parent.saveItem.show()
#             # rightLayout = QHBoxLayout()
#
#             self.parent.rightLayout.addWidget(item.widget)
#
#             # QWidget().layout()
#             # if self.parent.widget_2
#
#
#
#             # self.parent.widget_2.setLayout(rightLayout)
#
#
#
#
# class customWidgetItem(QWidget):
#     def __init__(self, type ,parent=None):
#         super(customWidgetItem, self).__init__(parent)
#         self.textQVBoxLayout = QVBoxLayout()
#         self.textUpQLabel = QLabel()
#         self.textDownQLabel = QLabel()
#         self.textQVBoxLayout.addWidget(self.textUpQLabel)
#         self.textQVBoxLayout.addWidget(self.textDownQLabel)
#         self.allQHBoxLayout = QHBoxLayout()
#         self.iconQLabel = QLabel()
#
#         self.button = QPushButton()
#         self.line = QLineEdit()
#         self.parent = parent
#
#         self.widget = customListWidget(type=Type.right,parent=self.parent.parent)
#
#         self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
#         self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
#         self.allQHBoxLayout.addWidget(self.button, 2)
#         self.allQHBoxLayout.addWidget(self.line, 3)
#         # self.allQHBoxLayout.addWidget(self.widget, 4)
#         self.setLayout(self.allQHBoxLayout)
#         # setStyleSheet
#         self.textUpQLabel.setStyleSheet('''
#             color: rgb(0, 0, 255);
#         ''')
#         self.textDownQLabel.setStyleSheet('''
#             color: rgb(255, 0, 0);
#         ''')
#
#     def setTextUp(self, text):
#         self.textUpQLabel.setText(text)
#
#     def setTextDown(self, text):
#         self.textDownQLabel.setText(text)
#
#     def setIcon(self, imagePath):
#         self.iconQLabel.setPixmap(QPixmap(imagePath))
#
#
#
# class labelWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         loadUi("label.ui", self)
#
#
#         self.leftListWidget = customListWidget(type=Type.left,parent=self)
#         # rightListWidget = customListWidget(type=Type.right,parent=self)
#
#         self.leftLayout = QHBoxLayout()
#         self.rightLayout= QHBoxLayout()
#         self.leftLayout.addWidget(self.leftListWidget)
#         # rightLayout.addWidget(rightListWidget)
#         self.widget.setLayout(self.leftLayout)
#         self.widget_2.setLayout(self.rightLayout)
#
#
#         self.saveItemName = None
#
#
#         for data in [
#             ('No.1', 'Meyoko',  'icon.png'),
#             ('No.2', 'Nyaruko', 'icon.png'),
#             ('No.3', 'Louise',  'icon.png')]:
#             leftListWidgetItem = QListWidgetItem(self.leftListWidget)
#             # store the data needed to create/re-create the custom widget
#             leftListWidgetItem.setData(Qt.UserRole, data)
#             self.leftListWidget.addItem(leftListWidgetItem)
#             print(leftListWidgetItem)
#
#         print(self.leftListWidget)
#
#
#
# #
# #
# #
# # if __name__ == '__main__':
# #     app = QApplication([])
# #     win = labelWidget()
# #     win.show()
# #     app.exec_()
#
