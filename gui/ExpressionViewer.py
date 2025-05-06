from PyQt6.QtWidgets import QWidget, QHBoxLayout
from NodeViewerGenerator import NodeViewerGenerator


class ExpressionViewer(QWidget):
    def __init__(self, nodes, parent=None):
        super().__init__(parent)
        self._parent = parent
        self._nodes = nodes
        self._nodeViewers = []
        self._layout = QHBoxLayout()

        self._configure()
        self._displayNodes()

    def _configure(self):
        pass

    def _displayNodes(self):
        for node in self._nodes:
            nodeViewer = NodeViewerGenerator.getNodeViewer(node, self)
            self._nodeViewers.append(nodeViewer)
            self._layout.addWidget(nodeViewer)



