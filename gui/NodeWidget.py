from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal


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
    """

    input_mode_requested = pyqtSignal(object)   # payload : self
    action_committed = pyqtSignal(str, object)  # (nom_action, payload)

    def __init__(self, node_id):
        super().__init__()
        self.node_id = node_id

        self._stack = QStackedWidget()
        self._display_widget = self._build_display_widget()
        self._input_widget = self._build_input_widget()
        self._stack.addWidget(self._display_widget)
        self._stack.addWidget(self._input_widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._stack)
        self.setLayout(layout)

    def _build_display_widget(self) -> QWidget:
        raise NotImplementedError

    def _build_input_widget(self) -> QWidget:
        raise NotImplementedError

    def enter_display_mode(self):
        self._stack.setCurrentWidget(self._display_widget)

    def enter_input_mode(self):
        self._stack.setCurrentWidget(self._input_widget)

    def is_in_input_mode(self) -> bool:
        return self._stack.currentWidget() is self._input_widget

    def _request_input_mode(self):
        self.input_mode_requested.emit(self)

    def _commit_action(self, action: str, payload=None):
        self.action_committed.emit(action, payload)
        self.enter_display_mode()
