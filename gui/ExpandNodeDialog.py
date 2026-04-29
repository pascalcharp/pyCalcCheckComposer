from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt


class ExpandNodeDialog(QDialog):
    """
    Une boîte de dialogue unique pour l'expansion d'un ENode,
    affichant une grille d'opérateurs et un bouton "Annuler".
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configuration de base
        self.setWindowTitle("Sélectionner un opérateur")
        self.setMinimumSize(400, 300)

        # Layout principal (Vertical)
        main_layout = QVBoxLayout()

        # Ajout d'un label explicatif
        label = QLabel("Choisissez un opérateur pour étendre le noeud :")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label)

        # Grille pour les opérateurs
        grid_layout = QGridLayout()

        # Opérateurs à afficher (provenant de OpNode.BooleanOperators)
        self.operators = [
            "AndOperator", "OrOperator", "XorOperator",
            "ImplicationOperator", "ConsequenceOperator",
            "EquivalentOperator", "NotEquivalentOperator"
        ]

        # Dictionnaire pour stocker la correspondance des boutons
        self.selected_operator = None  # Stockera l'opérateur choisi

        # Ajouter les boutons pour chaque opérateur
        for i, operator in enumerate(self.operators):
            button = QPushButton(operator)  # Texte du bouton = clé de l'opérateur
            button.setFixedSize(100, 40)
            button.clicked.connect(lambda _, op=operator: self._on_operator_selected(op))
            grid_layout.addWidget(button, i // 3, i % 3)  # 3 colonnes dans la grille

        main_layout.addLayout(grid_layout)

        # Ajout d'un bouton "Annuler"
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.reject)  # Ferme la boîte sans rien retourner

        # Centrage du bouton "Annuler" sous la grille
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(cancel_button)
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def _on_operator_selected(self, operator):
        """
        Appelé lorsqu'un bouton d'opérateur est cliqué.
        """
        self.selected_operator = operator
        self.accept()  # Ferme la boîte de dialogue avec accept

    def get_selected_operator(self):
        """
        Renvoie l'opérateur sélectionné (ou None si annulé).
        """
        return self.selected_operator
