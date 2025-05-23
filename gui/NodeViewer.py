from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton

NODE_VIEWER_SIZE = 40

class NodeViewer(QPushButton):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._node = node

        self._configure()


    def _onClicked(self):
        print("clicked")

    def _configure(self):
        self.setFixedSize(NODE_VIEWER_SIZE, NODE_VIEWER_SIZE)
        self.setText(self._node.__str__())

    def getNode(self):
        return self._node





