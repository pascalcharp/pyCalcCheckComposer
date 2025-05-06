from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from gui.NodeViewerGenerator import NodeViewerGenerator


class ExpressionViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._nodes = []
        self._nodeViewers = []
        self._layout = QHBoxLayout()

        self._configure()

    def _configure(self):
        self.setGeometry(100, 100, 800, 600)
        self.setLayout(self._layout)

    def updateNodes(self, nodes):
        self._nodes = nodes

    def displayNodes(self):
        for node in self._nodes:
            nodeViewer = NodeViewerGenerator.getNodeViewer(node, self)
            self._nodeViewers.append(nodeViewer)
            self._layout.addWidget(nodeViewer)

    def configureActions(self):
        for nodeViewer in self._nodeViewers:
            nodeViewer.clicked.connect((lambda : self.onNodeViewerClicked(nodeViewer.getNode())))

    def onNodeViewerClicked(self, node):
        assert(hasattr(self._parent, 'nodeViewerClicked') and callable(self._parent.nodeViewerClicked))
        self._parent.nodeViewerClicked(node, self)



