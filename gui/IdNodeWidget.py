from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit
from gui.GuiConstants import GuiConstants
from gui.NodeWidget import NodeWidget


class IdNodeWidget(NodeWidget):

    def __init__(self, node_id, name):
        self._name = name              # doit être posé avant super().__init__()
        super().__init__(node_id)

    def _build_display_widget(self) -> QWidget:
        btn = QPushButton(self._name)
        btn.setFixedHeight(GuiConstants.NODE_DISPLAY_BUTTON_HEIGHT)
        btn.clicked.connect(self._request_input_mode)
        return btn

    def _build_input_widget(self) -> QWidget:
        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(GuiConstants.NODE_INPUT_LAYOUT_SPACING)

        self._name_input = QLineEdit(self._name)
        self._name_input.setFixedWidth(GuiConstants.NODE_TEXT_INPUT_WIDTH)
        self._name_input.returnPressed.connect(self._on_rename_confirmed)

        self._rename_confirm = QPushButton("✓")
        self._rename_confirm.setFixedSize(GuiConstants.NODE_ACTION_BUTTON_WIDTH,
                                          GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
        self._rename_confirm.clicked.connect(self._on_rename_confirmed)

        self._revert_button = QPushButton("→E")
        self._revert_button.setFixedHeight(GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
        self._revert_button.clicked.connect(lambda: self._commit_action("revert"))

        self._cancel_button = QPushButton("✕")
        self._cancel_button.setFixedSize(GuiConstants.NODE_ACTION_BUTTON_WIDTH,
                                         GuiConstants.NODE_INPUT_BUTTON_HEIGHT)
        self._cancel_button.clicked.connect(self.enter_display_mode)

        layout.addWidget(self._name_input)
        layout.addWidget(self._rename_confirm)
        layout.addWidget(self._revert_button)
        layout.addWidget(self._cancel_button)
        container.setLayout(layout)
        return container

    def _on_rename_confirmed(self):
        name = self._name_input.text().strip()
        if name:
            self._commit_action("rename", name)
