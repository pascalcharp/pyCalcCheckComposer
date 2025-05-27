import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton

from BooleanExpression.Node.ENode import ENode
from gui.BinaryOperatorProductionChooser import BinaryOperatorProductionChooser
from gui.NodeViewer import NodeViewer



class ENodeViewer(NodeViewer):
    def __init__(self, enode, parent=None):
        assert(isinstance(enode, ENode))
        super().__init__(enode, parent)

        self._layoutActive = QVBoxLayout()
        self._productionButtons = [QPushButton() for _ in range(3)]

        self._configure()
        self._configureActions()


    def _configure(self):
        super()._configure()
        for button in self._productionButtons:
            button.setText("Button")
            self._layoutActive.addWidget(button)

    def _configureActions(self):
        self._nodeButton.clicked.connect(self.onClicked)

    def onClicked(self):
        super().onClicked()
        self.
        self.setLayout(self._layoutActive)


if __name__=="__main__":
    app = QApplication([])
    node = ENode()
    ENodeViewer(node).show()
    sys.exit(app.exec())


