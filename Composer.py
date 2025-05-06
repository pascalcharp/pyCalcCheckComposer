from BooleanExpression.ExpressionTree import BooleanExpressionTree

class Composer:
    def __init__(self, mainWindow):
        self._mainWindow = mainWindow
        self._expression = BooleanExpressionTree()
        self._configureActions()

        self.startGui()

    def startGui(self):
        self._mainWindow.show()

    def _configureActions(self):
        pass