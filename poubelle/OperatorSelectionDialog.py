from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel


class OperatorSelectionDialog(QDialog):
    """
    Une boîte de dialogue permettant à l'utilisateur de choisir un opérateur pour étendre un ENode.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Choisissez un opérateur")
        self.setMinimumSize(300, 150)

        # Créez les widgets
        layout = QVBoxLayout()

        label = QLabel("Sélectionnez un opérateur pour l'expansion :")
        layout.addWidget(label)

        # Liste déroulante avec les opérateurs
        self.operator_combo = QComboBox()
        self.operator_combo.addItems([
            "AndOperator",
            "OrOperator",
            "XorOperator",
            "ImplicationOperator",
            "ConsequenceOperator",
            "EquivalentOperator",
            "NotEquivalentOperator"
        ])
        layout.addWidget(self.operator_combo)

        # Bouton pour valider la sélection
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)  # Ferme la boîte lorsque validée
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_selected_operator(self):
        """
        Retourne l'opérateur sélectionné par l'utilisateur.
        """
        return self.operator_combo.currentText()
