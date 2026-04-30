from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel, QFrame, \
    QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import Qt
from controllers.ProofController import ProofController
from gui.ExpressionWidget import ExpressionWidget
from gui.GuiConstants import GuiConstants


class ProofWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Titre de la fenêtre
        self.setWindowTitle(GuiConstants.MAIN_WINDOW_TITLE)

        # Initialiser le contrôleur
        self.controller = ProofController(self)

        # Configuration de la taille de la fenêtre
        self._configure_window_size()

        # Scroll Area où toutes les expressions seront contenues
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(GuiConstants.LAYOUT_SPACING)
        self.layout.setContentsMargins(*GuiConstants.LAYOUT_MARGINS)
        self.spacer = QSpacerItem(GuiConstants.SPACER_WIDTH,
                                  GuiConstants.SPACER_HEIGHT,
                                  QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)
        self.layout.addSpacerItem(self.spacer)
        self.scroll_area_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)

        # Bouton pour ajouter une nouvelle expression
        self.add_expression_button = QPushButton(GuiConstants.ADD_EXPRESSION_BUTTON_TEXT)
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
        self.resize(screen_width // GuiConstants.INITIAL_WINDOW_WIDTH_RATIO, screen_height // GuiConstants.INITIAL_WINDOW_HEIGHT_RATIO)

        # Fixer une taille minimale par précaution
        self.setMinimumSize(GuiConstants.MINIMUM_WINDOW_WIDTH, GuiConstants.MINIMUM_WINDOW_HEIGHT)

    def add_expression_widget(self, expression_widget):
        """
        Ajoute un widget d'expression encapsulé dans un QFrame pour délimiter visuellement.
        """
        # Créez un cadre (QFrame) pour encapsuler le widget
        expression_frame = QFrame()
        expression_frame.setLayout(QVBoxLayout())

        # Ajoute le widget d'expression à l'intérieur du cadre
        expression_frame.layout().addWidget(expression_widget)

        # Génère le CSS personnalisé
        expression_frame_style = GuiConstants.EXPRESSION_FRAME_STYLE_TEMPLATE.format(
            border_color=GuiConstants.COLOR_BORDER,
            background_color=GuiConstants.COLOR_BACKGROUND
        )

        # Applique le style généré
        expression_frame.setStyleSheet(expression_frame_style)

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

    def display_error_message(self, message):
        QMessageBox.critical(self, "Erreur", message)




if __name__ == "__main__":
    app = QApplication([])
    window = ProofWindow()
    window.show()
    app.exec()
