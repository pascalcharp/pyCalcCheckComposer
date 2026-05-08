from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit
from gui.GuiConstants import GuiConstants
from gui.NodeWidget import NodeWidget

_ENODE_EXPANSIONS = [
    ("NotOperator",           "not E"),
    ("AndOperator",           "E and E"),
    ("OrOperator",            "E or E"),
    ("XorOperator",           "E ^ E"),
    ("ImplicationOperator",   "E impl E"),
    ("ConsequenceOperator",   "E cons E"),
    ("EquivalentOperator",    "E eq E"),
    ("NotEquivalentOperator", "E neq E"),
    ("Leftparen",             "(E)"),
]


class ENodeWidget(NodeWidget):

    def __init__(self, node_id):
        self._suggestion_buttons = []
        super().__init__(node_id)

    def _build_display_widget(self) -> QWidget:
        btn = QPushButton("?")
        s = GuiConstants.ENODE_DISPLAY_BUTTON_SIZE
        btn.setFixedSize(s, s)
        btn.clicked.connect(self._request_input_mode)
        return btn

    def _build_input_widget(self) -> QWidget:
        container = QWidget()
        p = GuiConstants.NODE_INPUT_CONTAINER_PADDING
        cols = GuiConstants.NODE_INPUT_GRID_COLUMNS
        layout = QGridLayout()
        layout.setContentsMargins(p, p, p, p)
        layout.setSpacing(GuiConstants.NODE_INPUT_LAYOUT_SPACING)

        self._op_buttons = {}
        for i, (op_key, label) in enumerate(_ENODE_EXPANSIONS):
            btn = QPushButton(label)
            btn.setFixedHeight(GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
            btn.clicked.connect(lambda _, k=op_key: self._commit_action("expand", k))
            self._op_buttons[op_key] = btn
            layout.addWidget(btn, i // cols, i % cols)

        self._var_row = len(_ENODE_EXPANSIONS) // cols
        self._var_input = QLineEdit()
        self._var_input.setPlaceholderText("variable")
        self._var_input.returnPressed.connect(self._on_var_confirmed)

        self._var_confirm = QPushButton("→")
        self._var_confirm.setFixedSize(GuiConstants.NODE_ACTION_BUTTON_WIDTH,
                                       GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
        self._var_confirm.clicked.connect(self._on_var_confirmed)

        layout.addWidget(self._var_input, self._var_row, 0, 1, cols - 1)
        layout.addWidget(self._var_confirm, self._var_row, cols - 1)
        container.setLayout(layout)
        return container

    def enter_display_mode(self):
        self._clear_suggestion_buttons()
        super().enter_display_mode()

    def set_variable_suggestions(self, names: list[str]):
        self._clear_suggestion_buttons()
        cols = GuiConstants.NODE_INPUT_GRID_COLUMNS
        layout = self._input_widget.layout()
        for i, name in enumerate(names):
            btn = QPushButton(name)
            btn.setFixedHeight(GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
            btn.clicked.connect(lambda _, n=name: self._commit_action("to_id", n))
            layout.addWidget(btn, self._var_row + 1 + i // cols, i % cols)
            self._suggestion_buttons.append(btn)

    def _clear_suggestion_buttons(self):
        layout = self._input_widget.layout()
        for btn in self._suggestion_buttons:
            layout.removeWidget(btn)
            btn.deleteLater()
        self._suggestion_buttons.clear()

    def _on_var_confirmed(self):
        name = self._var_input.text().strip()
        if name:
            self._var_input.clear()
            self._commit_action("to_id", name)
