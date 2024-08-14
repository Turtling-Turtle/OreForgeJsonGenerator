from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent, QPainter
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem

SCALE_FACTOR = 1.25


# class GridCanvas(QGraphicsView):
#     def __init__(self):
#         super().__init__()
#         self.scene = QGraphicsScene()
#         self.setScene(self.scene)
#         self.setRenderHints(QPainter.RenderHint.Antialiasing)
#         self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
#
#         self.zoomLeve = 1
#         self.dragging = False
#         self.last_mouse_pos = None
#
#     def addItem(self, item: QGraphicsItem) -> None:
#         self.scene.addItem(item)
#
#     def addNode(self, node):
#         self.nodes.append(node)
#         node.setParent(self)
#         node.show()
#
#     def paintEvent(self, event) -> None:
#         for item in self.scene.items():
#             item.paintEvent(event)
#         # painter = QPainter(self)
#         # for node in self.nodes:
#         #     node.paintEvent(event)
#         #     if node.nextNode is not None:
#         #         node.drawLine(node.rect.center(), node.nextNode.rect.center())
#
#     def mousePressEvent(self, event: QMouseEvent):
#         if event.buttons() == Qt.MouseButton.MiddleButton:
#             self.last_mouse_pos = event.pos()
#
#     def mouseMoveEvent(self, event: QMouseEvent):
#         if event.buttons() == Qt.MouseButton.LeftButton and self.last_mouse_pos:
#             delta = event.pos() - self.last_mouse_pos
#             self.last_mouse_pos = event.pos()
#
#             delta_scene = self.mapToScene(delta)
#             self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
#             self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
#
#     def mouseReleaseEvent(self, event: QMouseEvent):
#         if event.button() == Qt.MouseButton.LeftButton:
#             self.last_mouse_pos = None
class NodeViewer(QtWidgets.QGraphicsView):
    coordinatesChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super().__init__(parent)
        self._zoom = 0
        self._pinned = False
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self.last_mouse_pos = None

    def zoom(self, step):
        zoom = max(0, self._zoom + (step := int(step)))
        if zoom != self._zoom:
            self._zoom = zoom
            if self._zoom > 0:
                if step > 0:
                    factor = SCALE_FACTOR ** step
                else:
                    factor = 1 / SCALE_FACTOR ** abs(step)
                self.scale(factor, factor)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.zoom(delta and delta // abs(delta))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.move(event.pos())
            print("Clicked")
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event):
        print("Moving!")
        if event.button() == Qt.MouseButton.LeftButton:
            delta = event.pos() - self.last_mouse_pos
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y())
            self.last_mouse_pos = event.pos()

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)

    def updateCoordinates(self, pos=None):
        point = QPoint()
        self.coordinatesChanged.emit(point)

    def mouseMoveEvent(self, event):
        self.updateCoordinates(event.position().toPoint())
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.coordinatesChanged.emit(QPoint())
        super().leaveEvent(event)
