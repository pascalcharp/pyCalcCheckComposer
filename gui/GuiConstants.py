class GuiConstants:
    """Classe contenant les constantes utilisées dans la GUI."""

    COLOR_NODE_BUTTON_BACKGROUND = "#4CAF50"
    COLOR_NODE_BUTTON_TEXT = "white"
    COLOR_NODE_BUTTON_BORDER = "#45a049"
    COLOR_NODE_BUTTON_HOVER = "#45a049"

    # ExpandNodeDialog
    DIALOG_TITLE = "Développer l'expression"
    DIALOG_MIN_WIDTH = 400
    DIALOG_MIN_HEIGHT = 300
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 40
    CANCEL_BUTTON_TEXT = "Annuler"

    # Dimensions de la grille pour l'ExpandNodeDialog
    GRID_COLUMNS = 3  # Nombre de colonnes dans le layout de la grille
    GRID_BUTTON_MAX = 9  # Optionnel : Limite pour le nombre total de boutons (utile pour éviter d'exploser la grille)

    # ProofWindow
    MAIN_WINDOW_TITLE = "Preuve GUI"
    INITIAL_WINDOW_WIDTH_RATIO = 3
    INITIAL_WINDOW_HEIGHT_RATIO = 3
    MINIMUM_WINDOW_WIDTH = 600
    MINIMUM_WINDOW_HEIGHT = 400
    LAYOUT_SPACING = 10
    LAYOUT_MARGINS = (10, 10, 10, 10)
    SPACER_WIDTH = 20
    SPACER_HEIGHT = 20
    SPACER_HORIZONTAL_POLICY = "QSizePolicy.Policy.Minimum"
    SPACER_VERTICAL_POLICY = "QSizePolicy.Policy.Expanding"
    COLOR_BORDER = "#4CAF50"
    COLOR_BACKGROUND = "#f9f9f9"
    EXPRESSION_FRAME_STYLE_TEMPLATE = """
        QFrame {{
            border: 2px solid {border_color};  /* Couleur des bordures */
            border-radius: 8px;              /* Coins arrondis */
            background-color: {background_color};  /* Couleur de fond */
            margin: 10px;                    /* Espace autour du rectangle */
        }}
    """
    ADD_EXPRESSION_BUTTON_TEXT = "Ajouter une nouvelle expression"

    # --- Constants for ExpressionWidget ---
    BUTTON_OPERATOR_WIDTH = 40
    BUTTON_OPERATOR_HEIGHT = 40
    BUTTON_OPACITY_DISABLED = 0.5
    NODE_BUTTON_TEXT = "E"
    NODE_ALIGNMENT = "Qt.AlignmentFlag.AlignCenter"  # Utilisé dans les layouts

    STYLE_BUTTON_NODE = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 1px solid #45a049;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

    STYLE_BUTTON_NODE_TEMPLATE = """
        QPushButton {{
            background-color: {background_color};  /* Couleur de fond normale */
            color: {text_color};                  /* Couleur du texte */
            border: 1px solid {border_color};     /* Couleur de la bordure */
            border-radius: 8px;                   /* Coins arrondis */
            font-weight: bold;                    /* Texte en gras */
            font-size: 16px;                      /* Taille du texte */
        }}
        QPushButton:hover {{
            background-color: {hover_color};      /* Couleur lors du survol */
        }}
    """


