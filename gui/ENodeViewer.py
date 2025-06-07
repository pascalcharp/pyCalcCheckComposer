import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton

from BooleanExpression.Node.ENode import ENode
from gui.BinaryOperatorProductionChooser import BinaryOperatorProductionChooser
from gui.NodeViewer import NodeViewer



class ENodeViewer(NodeViewer):
    def __init__(self, enode, parent=None):
        assert(isinstance(enode, ENode))
        super().__init__(enode, parent)

        self._modes = ["inactive", "active"]
        self._layouts = {"active": QVBoxLayout(), "inactive": QVBoxLayout()}

        self._nodeButton = QPushButton(parent=self, text=self._node.__str__())
        self._productionChooser = BinaryOperatorProductionChooser(parent=self)

        self._configure()
        self._configureActions()



    def _configure(self):
        super()._configure()
        self._nodeButton.setFixedSize(100, 20)
        self._layouts["active"].addWidget(self._productionChooser)
        self._layouts["inactive"].addWidget(self._nodeButton)
        self.setLayout(self._layouts["inactive"])

    def setMode(self, mode):
        if mode in self._modes:
            self.setLayout(self._layouts[mode])
        else:
            raise ValueError("Invalid mode")


    def _configureActions(self):
        #self._nodeButton.clicked.connect(self.onNodeButtonClicked)
        pass


    def onNodeButtonClicked(self):
        super().onClicked()
        self.setMode("active")


if __name__=="__main__":
    app = QApplication([])
    node = ENode()
    ENodeViewer(node).show()
    sys.exit(app.exec())


