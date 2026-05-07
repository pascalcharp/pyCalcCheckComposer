from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal, QEvent, Qt
from gui.GuiConstants import GuiConstants


class NodeWidget(QWidget):
    """
    Widget de base pour un nœud d'expression booléenne.

    Deux modes :
      - Display : affiche le lexème du nœud ; un clic émet input_mode_requested.
      - Input   : affiche les options d'action ; un choix émet action_committed
                  et revient automatiquement en mode Display.

    Les sous-classes implémentent _build_display_widget() et _build_input_widget().
    ExpressionWidget écoute input_mode_requested pour garantir qu'un seul nœud
    est en mode Input à la fois.

    Implémentation : les deux widgets coexistent dans le même QHBoxLayout.
    Celui qui est inactif est caché ET marqué Ignored pour ne pas influencer
    la taille du layout. updateGeometry() propage le changement au parent.
    """

    input_mode_requested = pyqtSignal(object)   # payload : self
    action_committed = pyqtSignal(str, object)  # (nom_action, payload)
    selection_toggled = pyqtSignal(object)       # payload : self

    def __init__(self, node_id):
        super().__init__()
        self.node_id = node_id
        self._is_in_input_mode = False
        self._is_selected = False

        self._display_widget = self._build_display_widget()
        self._input_widget = self._build_input_widget()

        # Encadrement visuel du mode Input : le style vient de APP_STYLESHEET via l'objectName.
        self._input_widget.setObjectName("nodeInput")

        # Le widget Input démarre caché et ignoré par le layout.
        self._input_widget.hide()
        self._input_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._display_widget)
        layout.addWidget(self._input_widget)
        self.setLayout(layout)

        # Garantit l'état initial Display sur toutes les plateformes.
        self._display_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self._display_widget.show()

        # Intercepte le Ctrl+clic avant que le bouton ne le traite.
        self._display_widget.installEventFilter(self)

    def _build_display_widget(self) -> QWidget:
        raise NotImplementedError

    def _build_input_widget(self) -> QWidget:
        raise NotImplementedError

    def enter_display_mode(self):
        self._input_widget.hide()
        self._input_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self._display_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self._display_widget.show()
        self._is_in_input_mode = False
        self.updateGeometry()

    def enter_input_mode(self):
        self._display_widget.hide()
        self._display_widget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self._input_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self._input_widget.show()
        self._is_in_input_mode = True
        self.updateGeometry()

    def is_in_input_mode(self) -> bool:
        return self._is_in_input_mode

    def eventFilter(self, obj, event):
        if (obj is self._display_widget
                and event.type() == QEvent.Type.MouseButtonPress
                and event.button() == Qt.MouseButton.LeftButton
                and event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.set_selected(not self._is_selected)
            self.selection_toggled.emit(self)
            return True   # consomme l'événement : le bouton n'ouvre pas le mode Input
        return False

    def set_selected(self, selected: bool):
        self._is_selected = selected
        if selected:
            self._display_widget.setStyleSheet(
                f"QPushButton {{"
                f"  background-color: {GuiConstants.COLOR_SELECTED_BG};"
                f"  color: {GuiConstants.COLOR_TEXT};"
                f"  border: 1px solid {GuiConstants.COLOR_SELECTED_BORDER};"
                f"  border-radius: 4px;"
                f"  padding: 2px 6px;"
                f"}}"
            )
        else:
            self._display_widget.setStyleSheet("")

    def is_selected(self) -> bool:
        return self._is_selected

    def _request_input_mode(self):
        self.input_mode_requested.emit(self)

    def _commit_action(self, action: str, payload=None):
        self.action_committed.emit(action, payload)
        self.enter_display_mode()
