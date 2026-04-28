from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel
from PyQt6.QtCore import Qt
from controllers.ProofController import ProofController


class ProofWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Titre de la fenêtre
        self.setWindowTitle("Preuve GUI")

        # Initialiser le contrôleur
        self.controller = ProofController(self)

        # Configuration de la taille de la fenêtre
        self._configure_window_size()

        # Scroll Area où toutes les expressions seront contenues
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.scroll_area_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)

        # Bouton pour ajouter une nouvelle expression
        self.add_expression_button = QPushButton("Ajouter une nouvelle expression")
        self.add_expression_button.clicked.connect(self.controller.add_new_expression)

        # Layout principal
        header_layout = QVBoxLayout()
        header_layout.addWidget(self.add_expression_button)
        header_layout.addWidget(self.scroll_area)

        container = QWidget()
        container.setLayout(header_layout)
        self.setCentralWidget(container)

    def _configure_window_size(self):
        """
        Configure la taille initiale de la fenêtre principale en fonction de l'écran de l'utilisateur.
        """
        # Obtenir la résolution de l'écran principal
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # Fixer la taille à un tiers de la largeur et de la hauteur de l'écran
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        self.resize(screen_width // 3, screen_height // 3)

        # Fixer une taille minimale par précaution
        self.setMinimumSize(600, 400)

    def add_expression_widget(self, expression_widget):
        """
        Ajoute un nouveau widget d'expression à la fenêtre.
        """
        self.layout.addWidget(expression_widget)

    def update_expression_widget(self, expression_index):
        """
        Rafraîchit un widget d'expression spécifique après modification.

        :param expression_index: Index du widget dans le layout.
        """
        widget = self.layout.itemAt(expression_index).widget()
        widget.repaint()

    def update_proof_display(self, expression_string):
        """
        Met à jour l'affichage d'une expression logique sous forme de texte.
        """
        label = QLabel(expression_string)
        self.layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication([])
    window = ProofWindow()
    window.show()
    app.exec()
