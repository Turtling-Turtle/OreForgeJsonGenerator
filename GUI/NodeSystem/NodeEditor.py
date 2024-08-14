from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QGraphicsScene, QGraphicsView

from GUI.NodeSystem.NodeViewer import NodeViewer
from GUI.NodeSystem.Node import Node


class NodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Custom Node System')
        self.setGeometry(100, 100, 800, 600)



        # self.graphicsView = QGraphicsView()
        # self.graphicsView.setUpdatesEnabled(True)
        self.scene = QGraphicsScene()
        self.viewer = NodeViewer(self.scene)
        self.setCentralWidget(self.viewer)

        self.scene.addItem(Node("Test 1", 250, 250, 300, 10))
        self.scene.addItem(Node("Test 2", 10, 200, 250, 10))
        self.scene.addItem(Node("Test 3", 100, 100, 100, 20))

        # central_widget = QWidget()
        self.setCentralWidget(self.viewer)

        # layout = QVBoxLayout()
        # central_widget.setLayout(layout)

        self.last_mouse_pos = None
        # self.canvas = GridCanvas()
        # layout.addWidget(self.graphicsView)
        # self.canvas.addNode(Node("Test 1", 30, 200, 200, 200))
        # self.canvas.addNode(Node("Test 2", 90, 200, 250, 250))

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self.last_mouse_pos = event.pos()
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.MouseButton.LeftButton:
    #         delta = event.pos() - self.last_mouse_pos
    #         self.graphicsView.horizontalScrollBar().setValue(
    #             self.graphicsView.horizontalScrollBar().value() - delta.x())
    #         self.graphicsView.verticalScrollBar().setValue(self.graphicsView.verticalScrollBar().value() - delta.y())
    #         self.last_mouse_pos = event.pos()

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         print("Clicked!")
    #         self.last_mouse_pos = event.pos()
    #
    # def mouseMoveEvent(self, event):
    #     print("Moving!")
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         print("Moving!")
    #         delta = event.pos() - self.last_mouse_pos
    #
    #         self.viewer.horizontalScrollBar().setValue(
    #             self.viewer.horizontalScrollBar().value() - delta.x())
    #         self.viewer.verticalScrollBar().setValue(
    #             self.viewer.verticalScrollBar().value() - delta.y())
    #         self.last_mouse_pos = event.pos()


# class NodeEditor(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.viewer = NodeViewer(self)
#         self.viewer.coordinatesChanged.connect(self.handleCoords)
#         self.labelCoords = QtWidgets.QLabel(self)
#         self.labelCoords.setAlignment(
#             QtCore.Qt.AlignmentFlag.AlignRight |
#             QtCore.Qt.AlignmentFlag.AlignCenter)
#         layout = QtWidgets.QGridLayout(self)
#         layout.addWidget(self.viewer, 0, 0, 1, 3)
#         layout.addWidget(self.labelCoords, 1, 2, 1, 1)
#         layout.setColumnStretch(2, 2)
#
#     def handleCoords(self, point):
#         self.labelCoords.setText(f'{90}, {90}')
#

if __name__ == '__main__':
    app = QApplication([])
    window = NodeEditor()
    window.show()
    app.exec()
