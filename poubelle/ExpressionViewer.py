from PyQt6.QtGui import QWindow
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QListWidgetItem
from gui.NodeViewerGenerator import NodeViewerGenerator
from BooleanExpression.ExpressionTree import BooleanExpressionTree



class ExpressionViewer(QWidget):
    def __init__(self, parent=None, expression_tree=None):
        super().__init__(parent)
        self._parent = parent
        if expression_tree is None:
            self._tree = BooleanExpressionTree()
        else:
            self._tree = expression_tree
        self.updateNodeViewers()
        self._layout = QHBoxLayout()
        self._configure()

    def _configure(self):
        self.setGeometry(100, 100, 800, 600)
        self.setLayout(self._layout)

    def _clearNodeViewers(self):
        for viewer in self._nodeViewers:
            viewer.hide()
            viewer.deleteLater()
        self._nodeViewers.clear()


    def updateNodeViewers(self):
        self._nodes = self._tree.get_expression()
        self._nodeViewers = [NodeViewerGenerator.getNodeViewer(node, self) for node in self._nodes]


def refreshViewer(self):
        if self._nodeViewers:
            self._clearNodeViewers()

        for node in self._nodes:
            nodeViewer = NodeViewerGenerator.getNodeViewer(node, self)
            self._nodeViewers.append(nodeViewer)
            self._layout.addWidget(nodeViewer)

        #self.configureActions()


    def configureActions(self):
        for nodeViewer in self._nodeViewers:
            nodeViewer.clicked.connect((lambda : self.onNodeViewerClicked(nodeViewer.getNode())))

    def onNodeViewerClicked(self, node):
        assert(hasattr(self._parent, 'nodeViewerClicked') and callable(self._parent.nodeViewerClicked))
        node.onClicked()
        self._parent.nodeViewerClicked(node, self)





