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

    # --- Palette générale ---
    COLOR_TEXT               = "#212121"
    COLOR_BUTTON_BG          = "#e8e8e8"
    COLOR_BUTTON_BG_HOVER    = "#d0d0d0"
    COLOR_BUTTON_BG_PRESSED  = "#bdbdbd"
    COLOR_BUTTON_DISABLED_FG = "#9e9e9e"
    COLOR_WIDGET_BORDER      = "#bdbdbd"
    COLOR_INPUT_BG           = "#ffffff"
    COLOR_SELECTED_BG        = "#ffe082"   # jaune ambré — nœud sélectionné
    COLOR_SELECTED_BORDER    = "#ffc107"   # bordure dorée — nœud sélectionné

    # --- Mode Input (encadrement visuel) ---
    NODE_INPUT_BORDER_COLOR      = "#4CAF50"
    NODE_INPUT_BACKGROUND_COLOR  = "#e8f5e9"

    # --- Famille NodeWidget ---
    ENODE_DISPLAY_BUTTON_SIZE   = 40
    NODE_DISPLAY_BUTTON_HEIGHT  = 40
    NODE_INPUT_BUTTON_HEIGHT    = 35
    NODE_ACTION_BUTTON_WIDTH    = 30
    NODE_INPUT_LAYOUT_SPACING   = 4
    NODE_INPUT_CONTAINER_PADDING = 4
    NODE_INPUT_GRID_COLUMNS     = 3

    # --- Stylesheet globale (appliquée sur QApplication, base Fusion) ---
    # Les doubles accolades {{ }} sont des accolades CSS littérales dans un f-string.
    APP_STYLESHEET = (
        f"QPushButton {{"
        f"  background-color: {COLOR_BUTTON_BG};"
        f"  color: {COLOR_TEXT};"
        f"  border: 1px solid {COLOR_WIDGET_BORDER};"
        f"  border-radius: 4px;"
        f"  padding: 2px 6px;"
        f"}}"
        f"QPushButton:hover {{"
        f"  background-color: {COLOR_BUTTON_BG_HOVER};"
        f"}}"
        f"QPushButton:pressed {{"
        f"  background-color: {COLOR_BUTTON_BG_PRESSED};"
        f"}}"
        f"QPushButton:disabled {{"
        f"  color: {COLOR_BUTTON_DISABLED_FG};"
        f"}}"
        f"QLineEdit {{"
        f"  background-color: {COLOR_INPUT_BG};"
        f"  color: {COLOR_TEXT};"
        f"  border: 1px solid {COLOR_WIDGET_BORDER};"
        f"  border-radius: 3px;"
        f"  padding: 2px 4px;"
        f"}}"
        f"QWidget#nodeInput {{"
        f"  border: 2px solid {NODE_INPUT_BORDER_COLOR};"
        f"  border-radius: 6px;"
        f"  background-color: {NODE_INPUT_BACKGROUND_COLOR};"
        f"}}"
    )
