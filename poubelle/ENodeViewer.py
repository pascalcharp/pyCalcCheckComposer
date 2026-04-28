import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QStackedWidget, QDialog

from BooleanExpression.Node.ENode import ENode
from gui.BinaryOperatorProductionChooser import BinaryOperatorProductionChooser
from gui.NodeViewer import NodeViewer



class ENodeViewer(QWidget):
    def __init__(self, enode, parent=None):
        assert(isinstance(enode, ENode))

        super().__init__(parent)
        self._node = enode

        self._nodeButton = QPushButton(str(self._node), self)
        self._productionChooser = BinaryOperatorProductionChooser(self)
        self._layout = QVBoxLayout()

        self._configure()
        self._configureActions()



    def _configure(self):
        self._nodeButton.setFixedSize(100, 30)
        self._layout.addWidget(self._nodeButton)
        self.setLayout(self._layout)


    def _configureActions(self):
        self._nodeButton.clicked.connect(self.onNodeButtonClicked)


    def onNodeButtonClicked(self):
        result = self._productionChooser.exec()
        if result == QDialog.DialogCode.Accepted:
            choice = self._productionChooser.getCurrentOperator()
            if choice is not None:
                print(choice)
        self._productionChooser.close()

if __name__=="__main__":
    app = QApplication([])
    node = ENode()

    viewer = ENodeViewer(node)
    viewer.setWindowTitle("ENodeViewer")
    viewer.setMinimumSize(400, 300)
    viewer.show()

    sys.exit(app.exec())


