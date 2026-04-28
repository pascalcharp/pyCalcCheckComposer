from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QColor, QPainter, QBrush
from PyQt6.QtCore import Qt


class NodeButton(QPushButton):
    """
    Représente un noeud graphique (ENode) sous forme de bouton cliquable.
    """

    def __init__(self, node_id, text, on_click):
        """
        Initialise un bouton représentant un noeud.

        :param node_id: ID unique du noeud associé.
        :param text: Texte affiché sur le bouton (ex. "E").
        :param on_click: Fonction déclenchée lors d'un clic.
        """
        super().__init__(text)
        self.node_id = node_id
        self.setFixedSize(50, 50)  # Taille du bouton (rectangle)
        self.setStyleSheet("background-color: lightblue; border: 1px solid black; border-radius: 5px;")
        self.clicked.connect(lambda: on_click(self.node_id))  # Connecter le clic à l'action

    def paintEvent(self, event):
        """
        Customise le rendu du bouton avec un fond bleu pâle et un texte centré.
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor("lightblue")))
        painter.drawRect(self.rect())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        painter.end()

