from PyQt6.QtWidgets import QWidget


class GridCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)
        node.setParent(self)
        node.show()

    def paintEvent(self, event) -> None:
        # painter = QPainter(self)
        for node in self.nodes:
            node.paintEvent(event)
            if node.nextNode is not None:
                node.drawLine(node.rect.center(), node.nextNode.rect.center())
