from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from config import configure


class tableBasicWidget(QTableWidget):
    def __init__(self, header, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.header = header
        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setStyleSheet("color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        self.setColumnWidth(1, 100)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #隐藏序号
        self.verticalHeader().hide()
        # 设置水平铺满
        self.horizontalHeader().setStretchLastSection(True)
        # 设置一行选中
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)


class tableColorWidget(tableBasicWidget):
    def __init__(self, header,parent=None,):
        super(tableColorWidget, self).__init__(header,parent)

        self.doubleClicked.connect(self.doubleClickEventHandle)


    def initRow(self):

        tags = configure["tag"]

        self.setRowCount(len(tags))

        for i ,v in enumerate(tags):
            self.setItem(i, 0, QTableWidgetItem(str(v["label"])))
            lab = QLabel()
            lab.setStyleSheet("border-radius:1px;background-color: rgba({0},{1},{2},{3});".format(v["color"][0],v["color"][1],v["color"][2],v["color"][3]))
            self.setCellWidget(i,1,lab)


    def doubleClickEventHandle(self, index):
        if len( self.header) == 1:
            return
        dialog = QColorDialog()
        widget = self.cellWidget(index.row(), 1)
        colorObject = dialog.getColor(widget.palette().window().color(),options=QColorDialog.ShowAlphaChannel)
        color = "({0},{1},{2},{3})".format(colorObject.red(),colorObject.green(),colorObject.blue(),colorObject.alpha())
        widget.setStyleSheet("border-radius:1px;background-color: rgba{0};".format(color))
        configure["tag"][index.row()]["color"] = [colorObject.red(),colorObject.green(),colorObject.blue(),colorObject.alpha()]
        print(configure)


class tableGraphicsWidget(tableBasicWidget):
    def __init__(self, header,parent=None,):
        super(tableGraphicsWidget, self).__init__(header,parent)

        self.doubleClicked.connect(self.doubleClickEventHandle)

    def doubleClickEventHandle(self, index):
        item = self.parent.viewer.GraphicsTypeDict[self.item(index.row(), 0).text()]

        if item["table_item"]["area"] is None:
            item["graph_item"].triggerSliderShow()
        else:
            item["graph_item"].triggerLinkerShow()

        # self.parent.viewer.GraphicsTypeDict[]

#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     qb = tableWidget()
#     qb.show()
#     sys.exit(app.exec_())
