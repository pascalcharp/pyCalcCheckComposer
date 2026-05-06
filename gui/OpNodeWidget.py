from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from BooleanExpression.Node.OpNode import BooleanOperators
from gui.GuiConstants import GuiConstants
from gui.NodeWidget import NodeWidget

_BINARY_OPERATORS = frozenset({
    "AndOperator", "OrOperator", "XorOperator",
    "ImplicationOperator", "ConsequenceOperator",
    "EquivalentOperator", "NotEquivalentOperator",
})

_BINARY_OPERATOR_ORDER = [
    "AndOperator", "OrOperator", "XorOperator",
    "ImplicationOperator", "ConsequenceOperator",
    "EquivalentOperator", "NotEquivalentOperator",
]


class OpNodeWidget(NodeWidget):

    def __init__(self, node_id, op_key):
        self._op_key = op_key          # doit être posé avant super().__init__()
        super().__init__(node_id)

    def _build_display_widget(self) -> QWidget:
        btn = QPushButton(BooleanOperators[self._op_key].strip())
        btn.setFixedHeight(GuiConstants.NODE_DISPLAY_BUTTON_HEIGHT)
        if self._op_key in _BINARY_OPERATORS:
            btn.clicked.connect(self._request_input_mode)
        else:
            btn.setEnabled(False)
        return btn

    def _build_input_widget(self) -> QWidget:
        container = QWidget()
        p = GuiConstants.NODE_INPUT_CONTAINER_PADDING
        cols = GuiConstants.NODE_INPUT_GRID_COLUMNS
        layout = QGridLayout()
        layout.setContentsMargins(p, p, p, p)
        layout.setSpacing(GuiConstants.NODE_INPUT_LAYOUT_SPACING)

        self._alt_buttons = {}
        alts = [k for k in _BINARY_OPERATOR_ORDER if k != self._op_key]
        for i, alt_key in enumerate(alts):
            btn = QPushButton(BooleanOperators[alt_key].strip())
            btn.setFixedHeight(GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
            btn.clicked.connect(lambda _, k=alt_key: self._commit_action("change_op", k))
            self._alt_buttons[alt_key] = btn
            layout.addWidget(btn, i // cols, i % cols)

        n = len(alts)
        self._cancel_button = QPushButton("✕")
        self._cancel_button.setFixedSize(GuiConstants.NODE_ACTION_BUTTON_WIDTH,
                                         GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
        self._cancel_button.clicked.connect(self.enter_display_mode)
        layout.addWidget(self._cancel_button, n // cols, n % cols)

        container.setLayout(layout)
        return container
