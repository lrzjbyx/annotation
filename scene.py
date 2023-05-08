
from PyQt5.QtCore import pyqtSignal, QPointF, Qt
from PyQt5.QtWidgets import QGraphicsScene, QUndoCommand, QGraphicsItem

from item import GraphicsBasicItem, PaintState


class PhotoScene(QGraphicsScene):
    itemChanged = pyqtSignal(GraphicsBasicItem, dict)
    addItemSignal = pyqtSignal(GraphicsBasicItem)
    # onAddItem

    def __init__(self,args):
        super(PhotoScene, self).__init__(args)
        self.item = None
        self.oldPos = QPointF()


    def mousePressEvent(self, event):
        mousePos = QPointF(event.buttonDownScenePos(Qt.LeftButton).x(),
                           event.buttonDownScenePos(Qt.LeftButton).y())
        itemList = self.items(mousePos)
        if len(itemList) > 0:
            self.item = itemList[0]
        if (self.item is not None) & (event.button() == Qt.LeftButton):
            self.oldPos = self.item.pos()

        super(PhotoScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if (self.item is not None) & (event.button() == Qt.LeftButton):
            if self.oldPos != self.item.pos():
                points = {"x":self.oldPos.x(),"y":self.oldPos.y()}
                self.itemChanged.emit(self.item, points)
                self.item.state = PaintState.none

            self.item = None

        super(PhotoScene, self).mouseReleaseEvent(event)





class ChangeCommand(QUndoCommand):
    def __init__(self, item, old_info_dict):
        super(ChangeCommand, self).__init__()
        self.item = item
        # self.oldPos = oldPos
        self.old_info_dict = old_info_dict
        # [self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height()]
        # self.new_info_dict = {
        #     "x": self.item.x()+self.item.rect().x,
        #     "y": self.item.y()+self.item.rect().y,
        #     "w": self.item.rect().w,
        #     "h": self.item.rect().h,
        #     "a": self.item.angle
        # }


    def redo(self):
        # self.item.
        # QGraphicsItem().setX()

        # self.item.setPos(self.newPos)
        print('移动图元 redo')
        # self.setText('移动图元 %d %d' % (self.item.pos().x(), self.item.pos().y()))

    def undo(self):
        # self.item.setPos(self.oldPos)
        print('移动图元----> undo')


class AddCommand(QUndoCommand):
    def __init__(self, scene ,item):
        super(AddCommand, self).__init__()
        self.item = item
        self.scene = scene

    def redo(self):
        # self.item.setPos(self.newPos)
        print('AddCommand redo')
        # self.setText('移动图元 %d %d' % (self.item.pos().x(), self.item.pos().y()))

    def undo(self):
        # self.item.setPos(self.oldPos)
        print('AddCommand----> undo')