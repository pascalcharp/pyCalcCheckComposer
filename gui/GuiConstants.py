class GuiConstants:
    """Classe contenant les constantes utilisées dans la GUI."""

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
    COLOR_BORDER = "#4CAF50"
    COLOR_BACKGROUND = "#f9f9f9"
    EXPRESSION_FRAME_STYLE_TEMPLATE = """
        QFrame {{
            border: 2px solid {border_color};
            border-radius: 8px;
            background-color: {background_color};
            margin: 10px;
        }}
    """
    ADD_EXPRESSION_BUTTON_TEXT = "Ajouter une nouvelle expression"
