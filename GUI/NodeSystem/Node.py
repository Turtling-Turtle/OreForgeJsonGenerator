import abc
from typing import Union

from PyQt6.QtCore import QRect, Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtWidgets import QWidget, QGraphicsItem, QGraphicsProxyWidget

from GUI.Validators.Validator import ValidationResult


class Node(QGraphicsProxyWidget):
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        super().__init__(parent=None)
        self.name = name
        self.rect = QRect(x, y, width, height)
        self.dragging = False
        self.nextNode = None

        self.setFlag(QGraphicsProxyWidget.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsProxyWidget.GraphicsItemFlag.ItemIsSelectable, True)
        self.offset = QPoint()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRect(self.rect)

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.drawRect(self.rect)

    def connectNode(self, node) -> None:
        self.nextNode = node

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            pass

    def mouseReleaseEvent(self, event):
        self.dragging = False

    @abc.abstractmethod
    def validate(self) -> Union[ValidationResult, list[ValidationResult]]:
        pass

    @abc.abstractmethod
    def toDict(self) -> dict:
        pass
