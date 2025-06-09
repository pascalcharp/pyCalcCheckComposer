import sys

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QApplication, QDialog, QDialogButtonBox
from PyQt6.QtCore import Qt

from BooleanExpression.Node.OpNode import BooleanOperators



class BinaryOperatorProductionChooser(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._currentOperator = None
        self._layout = QGridLayout()
        self._buttons = {}
        self._label = QLabel()
        self._okButton = QPushButton("OK")
        self._cancelButton = QPushButton("Cancel")
        self._configure()

    def _configure(self):
        self._layout.addWidget(self._label, 0, 0, 1, 2)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for key, loc in [
            ("AndOperator", (1, 0)),
            ("OrOperator", (1, 1)),
            ("ImplicationOperator", (2, 0)),
            ("ConsequenceOperator", (2, 1)),
            ("EquivalentOperator", (3, 0)),
            ("NotEquivalentOperator", (3, 1))
        ]:
            self._buttons.update({key: QPushButton(key[0])})
            self._buttons[key].setFixedSize(100, 30)
            self._layout.addWidget(self._buttons[key], loc[0], loc[1])

        self._layout.addWidget(self._okButton, 4, 0)
        self._layout.addWidget(self._cancelButton, 4, 1)
        self.setLayout(self._layout)

        for key, button in self._buttons.items():
            button.clicked.connect(lambda checked, k=key: self._onButtonClicked(k))

        self._okButton.clicked.connect(self.accept)
        self._cancelButton.clicked.connect(self.reject)


    def _onButtonClicked(self, key):
        self._currentOperator = key
        self._label.setText(key[0])


    def getCurrentOperator(self):
        return self._currentOperator

if __name__ == "__main__":
    app = QApplication([])
    chooser = BinaryOperatorProductionChooser()
    result = chooser.exec()
    if result == QDialog.DialogCode.Accepted:
        print("Accepted")
        choice = chooser.getCurrentOperator()
        if choice is not None:
            print(choice)
        else:
            print("No choice")
    else:
        print("Cancelled")
    sys.exit(app.exec())



