from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFrame, \
    QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from controllers.ProofController import ProofController
from gui.ExpressionWidget import ExpressionWidget
from gui.OperatorSelectionDialog import OperatorSelectionDialog


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
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addSpacerItem(self.spacer)
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
        Ajoute un widget d'expression encapsulé dans un QFrame pour délimiter visuellement.
        """
        # Créez un cadre (QFrame) pour encapsuler le widget
        expression_frame = QFrame()
        expression_frame.setLayout(QVBoxLayout())

        # Ajoute le widget d'expression à l'intérieur du cadre
        expression_frame.layout().addWidget(expression_widget)

        # Applique un style personnalisé au cadre
        expression_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #4CAF50;  /* BORDURE - Couleur verte */
                border-radius: 8px;         /* Coins arrondis */
                background-color: #f9f9f9;  /* Fond léger */
                margin: 10px;               /* Espace autour du rectangle */
            }
        """)

        # Ajoute le cadre au layout principal de ProofWindow
        self.layout.insertWidget(0, expression_frame)

    def update_expression_widget(self, expression_index):
        """
        Rafraîchit un widget d'expression spécifique après modification.

        :param expression_index: Index du widget dans le layout.
        """
        frame = self.layout.itemAt(expression_index).widget()
        assert isinstance(frame, QFrame)
        widget = frame.layout().itemAt(0).widget()
        assert isinstance(widget, ExpressionWidget)
        widget.render_expression()

    def update_proof_display(self, expression_string):
        """
        Met à jour l'affichage d'une expression logique sous forme de texte.
        """
        label = QLabel(expression_string)
        self.layout.addWidget(label)

    def select_operator(self):
        """
        Affiche une boîte de dialogue permettant à l'utilisateur de choisir un opérateur.

        :return: Le nom de l'opérateur sélectionné (str), ou None si l'utilisateur annule.
        """
        dialog = OperatorSelectionDialog(self)
        if dialog.exec():  # Si l'utilisateur clique sur OK
            return dialog.get_selected_operator()
        return None  # Retourne None si la boîte est annulée


if __name__ == "__main__":
    app = QApplication([])
    window = ProofWindow()
    window.show()
    app.exec()
