from BooleanExpression.ExpressionTree import BooleanExpressionTree
from gui.ComposerMainWindow import ComposerMainWindow


class Composer:
    def __init__(self):
        self._mainWindow = ComposerMainWindow(self)
        self._expression = BooleanExpressionTree()

        self.startGui()
        self._configureActions()


    def startGui(self):
        self._mainWindow.show()
        self._updateExpression(self._expression.get_expression())

    def _configureActions(self):
        self._mainWindow.configureActions()

    def _updateExpression(self, expression):
        self._mainWindow.updateExpression(expression)
