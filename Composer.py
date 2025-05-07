from BooleanExpression.ExpressionTree import BooleanExpressionTree
from gui.ComposerMainWindow import ComposerMainWindow


class Composer:
    def __init__(self):
        self._mainWindow = ComposerMainWindow(self)
        self._expression = BooleanExpressionTree()

        self.startGui()


    def startGui(self):
        self._updateExpression(self._expression.get_expression())
        self._configureActions()
        self._mainWindow.show()


    def _configureActions(self):
        """
        Demande à la fenêtre principale de connecter tous ses éléments aux actions appropriées.
        Returns:
            None

        """
        self._mainWindow.configureActions()


    def _updateExpression(self, expression):
        self._mainWindow.updateExpression(expression)

    def nodeViewerClicked(self, node, expression_id):
        self._expression.generate_id_production(node.node_id, "x")
        self._updateExpression(self._expression.get_expression())

