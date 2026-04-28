from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout

NODE_VIEWER_SIZE = 40

class NodeViewer(QWidget):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._node = node

    def _configure(self):
        pass

    def getNode(self):
        return self._node

    def onClicked(self):
        pass





