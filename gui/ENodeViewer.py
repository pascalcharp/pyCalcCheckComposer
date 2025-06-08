import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QStackedWidget

from BooleanExpression.Node.ENode import ENode
from gui.BinaryOperatorProductionChooser import BinaryOperatorProductionChooser
from gui.NodeViewer import NodeViewer



class ENodeViewer(QStackedWidget):
    def __init__(self, enode, parent=None):
        assert(isinstance(enode, ENode))

        super().__init__(parent)
        self._node = enode

        self._modes = ["active", "inactive"]
        self._currentMode = "inactive"

        self._layouts = {"active": QVBoxLayout(), "inactive": QVBoxLayout()}
        self._viewers = {"active": QWidget(self), "inactive": QWidget(self)}

        self._nodeButton = QPushButton("E", self)
        self._productionChooser = BinaryOperatorProductionChooser(self)

        self._configure()
        self._configureActions()
        self.setMode(self._currentMode)



    def _configure(self):
        self._nodeButton.setFixedSize(100, 30)

        self._layouts["active"].addWidget(self._productionChooser)
        self._viewers["active"].setLayout(self._layouts["active"])
        self.addWidget(self._viewers["active"])

        self._layouts["inactive"].addWidget(self._nodeButton)
        self._viewers["inactive"].setLayout(self._layouts["inactive"])
        self.addWidget(self._viewers["inactive"])

    def setMode(self, mode):
        if mode in self._modes:
            self._currentMode = mode
            self.setCurrentIndex(self._modes.index(mode))
        else:
            raise ValueError("Invalid mode")


    def _configureActions(self):
        self._nodeButton.clicked.connect(self.onNodeButtonClicked)


    def onNodeButtonClicked(self):
        assert self._currentMode == "inactive"
        self.setMode("active")


if __name__=="__main__":
    app = QApplication([])
    node = ENode()

    viewer = ENodeViewer(node)
    viewer.setWindowTitle("ENodeViewer")
    viewer.setMinimumSize(400, 300)
    viewer.show()

    sys.exit(app.exec())


