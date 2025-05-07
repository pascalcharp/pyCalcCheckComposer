from PyQt6.QtWidgets import QMainWindow
from gui.ExpressionViewer import ExpressionViewer


class ComposerMainWindow(QMainWindow):
    def __init__(self, composer):
        super().__init__(parent=None)
        self._composer = composer
        self._viewer = ExpressionViewer(self)
        self.setWindowTitle("Composer")
        self.setCentralWidget(self._viewer)

    def updateExpression(self, expression):
        self._viewer.updateNodes(expression)
        self._viewer.refreshViewer()

    def configureActions(self):
        self._viewer.configureActions()

    def nodeViewerClicked(self, node, nodeViewer):
        self._composer.nodeViewerClicked(node, 0)

