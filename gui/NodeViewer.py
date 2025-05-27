from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout

NODE_VIEWER_SIZE = 40

class NodeViewer(QWidget):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._node = node
        self._nodeButton = QPushButton()
        self._layoutInactive = QVBoxLayout()



    def onClicked(self):
        print("clicked")

    def _configure(self):
        self._nodeButton.setFixedSize(NODE_VIEWER_SIZE, NODE_VIEWER_SIZE)
        self._nodeButton.setText(self._node.__str__())
        self._layoutInactive.addWidget(self._nodeButton)
        self.setLayout(self._layoutInactive)

    def getNode(self):
        return self._node





