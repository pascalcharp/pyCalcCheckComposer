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

    # --- Mode Input (encadrement visuel) ---
    NODE_INPUT_BORDER_COLOR = "#4CAF50"
    NODE_INPUT_BACKGROUND_COLOR = "#e8f5e9"
    NODE_INPUT_CONTAINER_STYLE = (
        "QWidget#nodeInput {{"
        " border: 2px solid {border_color};"
        " border-radius: 6px;"
        " background-color: {background_color};"
        " padding: 2px;"
        "}}"
    )

    # --- Famille NodeWidget ---
    ENODE_DISPLAY_BUTTON_SIZE = 40      # bouton "?" carré (ENodeWidget)
    NODE_DISPLAY_BUTTON_HEIGHT = 40     # hauteur bouton Display (OpNodeWidget, IdNodeWidget)
    NODE_INPUT_BUTTON_HEIGHT = 35       # hauteur de tous les boutons en mode Input
    NODE_ACTION_BUTTON_WIDTH = 30       # largeur des petits boutons ✓ → ✕
    NODE_TEXT_INPUT_WIDTH = 80          # largeur des champs texte variable / nom
    NODE_INPUT_LAYOUT_SPACING = 4       # espacement du layout en mode Input
