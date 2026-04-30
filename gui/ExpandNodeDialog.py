from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
from BooleanExpression.Node.OpNode import BooleanOperators
from gui.GuiConstants import GuiConstants


class ExpandNodeDialog(QDialog):
    """
    Une boîte de dialogue unique pour l'expansion d'un ENode,
    affichant une grille d'opérateurs et un bouton "Annuler".
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configuration de base
        self.setWindowTitle(GuiConstants.DIALOG_TITLE)
        self.setMinimumSize(GuiConstants.DIALOG_MIN_WIDTH, GuiConstants.DIALOG_MIN_HEIGHT)
        self.setWindowOpacity(0.5)

        # Layout principal (Vertical)
        main_layout = QVBoxLayout()

        # Grille pour les opérateurs
        grid_layout = QGridLayout()

        # Opérateurs à afficher (provenant de OpNode.BooleanOperators)
        self.operators = BooleanOperators.keys()

        # Dictionnaire pour stocker la correspondance des boutons
        self.selected_operator = None  # Stockera l'opérateur choisi

        # Ajouter les boutons pour chaque opérateur
        for i, operator in enumerate(self.operators):
            symbol = BooleanOperators[operator]
            if operator == "NotOperator":
                button_label = f"{symbol.strip()} E"
            elif operator in ["Leftparen", "Rightparen"]:
                continue
            else:
                button_label = f"E {symbol.strip()} E"
            button = QPushButton(button_label)  # Texte du bouton = clé de l'opérateur
            button.setFixedSize(GuiConstants.BUTTON_WIDTH, GuiConstants.BUTTON_HEIGHT)
            button.clicked.connect(lambda _, op=operator: self._on_operator_selected(op))
            grid_layout.addWidget(button, i // GuiConstants.GRID_COLUMNS, i % GuiConstants.GRID_COLUMNS)  # 3 colonnes dans la grille

        paren_button = QPushButton("(E)")
        paren_button.setFixedSize(GuiConstants.BUTTON_WIDTH, GuiConstants.BUTTON_HEIGHT)
        paren_button.clicked.connect(
            lambda: self._on_operator_selected("Leftparen")
        )
        grid_layout.addWidget(paren_button)
        main_layout.addLayout(grid_layout)

        # Ajout d'un bouton "Annuler"
        cancel_button = QPushButton(GuiConstants.CANCEL_BUTTON_TEXT)
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
