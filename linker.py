#
# from PyQt5.QtCore import QSize
# from PyQt5.QtWidgets import QWidget, QPushButton, QFormLayout, \
#     QLineEdit, QListWidget, QListWidgetItem, QCheckBox
#
#
# class CustomWidget(QWidget):
#
#     def __init__(self, item, *args, **kwargs):
#         super(CustomWidget, self).__init__(*args, **kwargs)
#         self.oldSize = None
#         self.item = item
#         layout = QFormLayout(self)
#         layout.addRow('我是label', QLineEdit(self))
#         layout.addRow('点击', QCheckBox(
#             '隐藏下面的按钮', self, toggled=self.hideChild))
#         self.button = QPushButton('我是被隐藏的', self)
#         layout.addRow(self.button)
#
#     def hideChild(self, v):
#         self.button.setVisible(not v)
#         # 这里很重要 当隐藏内部子控件时 需要重新计算高度
#         self.adjustSize()
#
#     def resizeEvent(self, event):
#         # 解决item的高度问题
#         super(CustomWidget, self).resizeEvent(event)
#         self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))
#
#
# class CustomButton(QPushButton):
#     # 按钮作为开关
#
#     def __init__(self, item, *args, **kwargs):
#         super(CustomButton, self).__init__(*args, **kwargs)
#         self.item = item
#         self.setCheckable(True)  # 设置可选中
#
#     def resizeEvent(self, event):
#         # 解决item的高度问题
#         super(CustomButton, self).resizeEvent(event)
#         self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))
#
#
# class Window(QListWidget):
#
#     def __init__(self, *args, **kwargs):
#         super(Window, self).__init__(*args, **kwargs)
#
#         for _ in range(3):
#             # 开关
#             item = QListWidgetItem(self)
#             btn = CustomButton(item, '折叠', self, objectName='testBtn')
#             self.setItemWidget(item, btn)
#
#             # 被折叠控件
#             item = QListWidgetItem(self)
#             # 通过按钮的选中来隐藏下面的item
#             btn.toggled.connect(item.setHidden)
#             self.setItemWidget(item, CustomWidget(item, self))
#
#
# if __name__ == '__main__':
#     import sys
#     import cgitb
#
#     cgitb.enable(format='text')
#     from PyQt5.QtWidgets import QApplication
#
#     app = QApplication(sys.argv)
#     # 通过qss改变按钮的高度
#     app.setStyleSheet('#testBtn{min-height:40px;}')
#     w = Window()
#     w.show()
#     sys.exit(app.exec_())
import sys

from PyQt5.QtCore import QSize, Qt, QModelIndex
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QWidget, QHBoxLayout, QApplication, \
    QListWidget, QListWidgetItem, QLabel, QComboBox, QHeaderView, QMenu, QMessageBox
from PyQt5.uic import loadUi

from config import configure
from tableWidget import tableBasicWidget


# class TableWidgetDragRows(QTableWidget):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
# 
#         self.setDragEnabled(True)
#         self.setAcceptDrops(True)
#         self.setSelectionBehavior(QAbstractItemView.SelectRows)
#         self.setDragDropOverwriteMode(False)
#         self.verticalHeader().hide()
#         self.horizontalHeader().setStyleSheet("color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
#         self.horizontalHeader().setStretchLastSection(True)
#         # self.setSelectionMode(QAbstractItemView.SingleSelection)
# 
#         self.last_drop_row = None
# 
#     # Override this method to get the correct row index for insertion
#     def dropMimeData(self, row, col, mimeData, action):
#         self.last_drop_row = row
#         return True
# 
# 
#     def dropEvent(self, event):
#         # The QTableWidget from which selected rows will be moved
#         sender = event.source()
# 
#         # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
#         super().dropEvent(event)
#         # Now we know where to insert selected row(s)
#         dropRow = self.last_drop_row
# 
#         selectedRows = sender.getselectedRowsFast()
# 
#         # Allocate space for transfer
#         for _ in selectedRows:
#             self.insertRow(dropRow)
# 
#         # if sender == receiver (self), after creating new empty rows selected rows might change their locations
#         sel_rows_offsets = [0 if self != sender or srow < dropRow else len(selectedRows) for srow in selectedRows]
#         selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]
# 
#         # copy content of selected rows into empty ones
#         for i, srow in enumerate(selectedRows):
#             for j in range(self.columnCount()):
#                 item = sender.item(srow, j)
#                 if item:
#                     source = QTableWidgetItem(item)
#                     self.setItem(dropRow + i, j, source)
# 
#         # delete selected rows
#         for srow in reversed(selectedRows):
#             sender.removeRow(srow)
# 
#         event.accept()
# 
# 
#     def getselectedRowsFast(self):
#         selectedRows = []
#         for item in self.selectedItems():
#             if item.row() not in selectedRows:
#                 selectedRows.append(item.row())
#         selectedRows.sort()
#         return selectedRows




class linkedTableWidgetDragRows(tableBasicWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropOverwriteMode(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        # self.setSelectionMode(QAbstractItemView.SingleSelection)

        self.last_drop_row = None

    # Override this method to get the correct row index for insertion
    def dropMimeData(self, row, col, mimeData, action):
        self.last_drop_row = row
        return True


    def dropEvent(self, event):
        # The QTableWidget from which selected rows will be moved
        sender = event.source()

        # Default dropEvent method fires dropMimeData with appropriate parameters (we're interested in the row index).
        super().dropEvent(event)
        # Now we know where to insert selected row(s)
        dropRow = self.last_drop_row

        selectedRows = sender.getselectedRowsFast()

        # Allocate space for transfer
        for _ in selectedRows:
            self.insertRow(dropRow)

        # if sender == receiver (self), after creating new empty rows selected rows might change their locations
        sel_rows_offsets = [0 if self != sender or srow < dropRow else len(selectedRows) for srow in selectedRows]
        selectedRows = [row + offset for row, offset in zip(selectedRows, sel_rows_offsets)]

        # copy content of selected rows into empty ones
        for i, srow in enumerate(selectedRows):
            for j in range(self.columnCount()):
                item = sender.item(srow, j)
                if item:
                    source = QTableWidgetItem(item)
                    self.setItem(dropRow + i, j, source)

        # delete selected rows
        for srow in reversed(selectedRows):
            sender.removeRow(srow)

        event.accept()


    def getselectedRowsFast(self):
        selectedRows = []
        for item in self.selectedItems():
            if item.row() not in selectedRows:
                selectedRows.append(item.row())
        selectedRows.sort()
        return selectedRows


class customLinkedWidget(QWidget):
    def __init__(self, item,groupCount, *args, **kwargs):
        super(customLinkedWidget, self).__init__(*args, **kwargs)
        self.item = item

        layout =  QHBoxLayout()

        self.label = QLabel()
        self.label.setText("组号{0}".format(groupCount))


        self.combobox =  QComboBox()
        self.combobox.addItems(configure["linked"])

        self.tablewidget = linkedTableWidgetDragRows(header=["标注id", "标注文本"],parent=self)

        layout.addWidget(self.label)
        layout.addWidget(self.combobox)
        layout.addWidget(self.tablewidget)
        self.setLayout(layout)

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(customLinkedWidget, self).resizeEvent(event)
        self.item.setSizeHint(QSize(300, 100))


class linkedListWidget(QListWidget):

    def __init__(self, *args, **kwargs):
        super(linkedListWidget, self).__init__(*args, **kwargs)
        self.groupCount = 1
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_click_menu)

    def add_group(self):
        item = QListWidgetItem(self)
        widget = customLinkedWidget(item,self.groupCount)
        self.groupCount +=1
        self.setItemWidget(item, widget)
        return  widget


    def del_group(self, checked: bool):
        try:
            row = self.currentRow()
            # self.fun()
            item = self.itemWidget(self.currentItem())
            # self.takeItem(row)
            if item.tablewidget.rowCount() == 0 :
                self.takeItem(row)
            else:
                QMessageBox.warning(self, "警告信息", "请先移除数据")


        except Exception as e:
            print(e)

    def right_click_menu(self,pos):
        try:
            item: QListWidgetItem = self.itemAt(pos)
            self._context_menu = QMenu()

            # 没有选中节点
            if item is None:
                self._action_add_group = self._context_menu.addAction(u'添加组')
                self._action_add_group.triggered.connect(self.add_group)
            else:
                # 删除组
                self._action_del_group = self._context_menu.addAction(u'删除组')
                self._action_del_group.triggered.connect(self.del_group)

            self._context_menu.exec_(self.mapToGlobal(pos))
        except Exception as e:
            print(e)



        # for i in item.tablewidget.rowCount():




class linker(QWidget):

    def __init__(self, item):
        super(linker, self).__init__(None)
        loadUi("./ui/linker.ui", self)
        self.item = item

        self.setWindowTitle(self.item.name)

        self.rightTable = linkedTableWidgetDragRows(parent=self, header=["标注id", "标注文本"])

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.rightTable)
        self.widget_4.setLayout(layout)


        self.leftList = linkedListWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.leftList)
        self.widget_3.setLayout(layout)

    def addGroup(self,data):
        widget = self.leftList.add_group()

        widget.combobox.setCurrentIndex(configure["linked"].index(data["relationship"]))

        for i, item in enumerate(data["links"]):
            c = QTableWidgetItem(item["name"])
            m = QTableWidgetItem(item["text"])

            widget.tablewidget.insertRow(widget.tablewidget.rowCount())
            widget.tablewidget.setItem(i, 0, c)
            widget.tablewidget.setItem(i, 1, m)



    def affiliate(self):
        d = {}
        for i in range(self.leftList.count()):
            item = self.leftList.item(i)
            widget = self.leftList.itemWidget(item)
            text = widget.label.text()
            d[text] = {
                "relationship":widget.combobox.currentText(),
                "affiliate":[]
            }
            for i in range(widget.tablewidget.rowCount()):
                d[text]["affiliate"].append(widget.tablewidget.item(i, 0).text())

        return d



    def loadLeftListItem(self):
        #  获取左侧的item
        self.rightTable.setRowCount(0)
        exlist = []
        for i in range(self.leftList.count()):
            item = self.leftList.item(i)
            widget = self.leftList.itemWidget(item)
            for i in range(widget.tablewidget.rowCount()):
                exlist.append(widget.tablewidget.item(i, 0).text())
                # print(widget.tablewidget.item(i, 0).text())
                # print(widget.tablewidget.item(i, 1).text())





        name =  self.item.name
        items = []
        for k,v in self.item.parent.RelationshipDict.items():
            if v["name"] == name:
                if k in exlist:
                    continue
                items.append((k,v["text"]))




        for i, (name, text) in enumerate(items):
            c = QTableWidgetItem(name)
            m = QTableWidgetItem(text)

            self.rightTable.insertRow(self.rightTable.rowCount())
            self.rightTable.setItem(i, 0, c)
            self.rightTable.setItem(i, 1, m)












#
# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         layout = QHBoxLayout()
#         self.setLayout(layout)
#
#         self.table_widgets = []
#
#         # tw = linkedTableWidgetDragRows(parent=self, header=["文本","关联"," "])
#         tw = linkedTableWidgetDragRows(parent=self, header=["标注id", "标注文本"])
#         # tw.setHorizontalHeaderLabels(['Colour', 'Model'])
#
#
#
#         self.table_widgets.append(tw)
#         layout.addWidget(tw)
#
#         ls = linkedListWidget()
#
#
#         layout.addWidget(ls)
#
#         filled_widget = self.table_widgets[0]
#         items = [('Red','Red', 'Toyota'), ('Blue','Blue', 'RV'), ('Green','Green','Beetle')]
#         for i, (colour, t ,model) in enumerate(items):
#             c = QTableWidgetItem(colour)
#             m = QTableWidgetItem(model)
#             d = QTableWidgetItem(t)
#
#             filled_widget.insertRow(filled_widget.rowCount())
#             filled_widget.setItem(i, 0, c)
#             filled_widget.setItem(i, 1, m)
#             # filled_widget.setItem(i, 2, d)
#
#
#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = linker(None)
    window.show()
    sys.exit(app.exec_())


