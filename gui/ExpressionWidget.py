from PyQt6.QtWidgets import QWidget, QHBoxLayout, QApplication, QMenu
from PyQt6.QtCore import Qt, QEvent

from BooleanExpression.Node.IdNode import IdNode
from BooleanExpression.Node.OpNode import OpNode, BooleanOperators

_ANNEX_OPERATOR_ORDER = [
    "AndOperator", "OrOperator", "XorOperator",
    "ImplicationOperator", "ConsequenceOperator",
    "EquivalentOperator", "NotEquivalentOperator",
]
from gui.ENodeWidget import ENodeWidget
from gui.IdNodeWidget import IdNodeWidget
from gui.OpNodeWidget import OpNodeWidget


class ExpressionWidget(QWidget):
    def __init__(self, expression_tree, proof_window, expression_index):
        super().__init__()
        self.tree = expression_tree
        self.proof_window = proof_window
        self.expression_index = expression_index
        self._active_node_widget = None
        self._selected_node_ids = set()
        self._node_widgets = {}        # node_id → NodeWidget

        self.node_layout = QHBoxLayout()
        self.render_expression()
        self.setLayout(self.node_layout)
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            # Un popup Qt (ex. QCompleter, menu contextuel système) capture la souris ;
            # laisser notre logique s'exécuter fermerait le widget actif avant que le
            # popup ait livré sa sélection, causant un crash ou une perte de saisie.
            if QApplication.activePopupWidget() is not None:
                return False

            pos = event.globalPosition().toPoint()

            if event.button() == Qt.MouseButton.RightButton:
                if self.rect().contains(self.mapFromGlobal(pos)):
                    if self._active_node_widget is not None:
                        self._active_node_widget.enter_display_mode()
                        self._active_node_widget = None
                    self._show_context_menu(pos)
                    return True

            elif event.button() == Qt.MouseButton.LeftButton:
                if not (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
                    self._clear_selection()
                if self._active_node_widget is not None:
                    nw = self._active_node_widget
                    if not nw.rect().contains(nw.mapFromGlobal(pos)):
                        nw.enter_display_mode()
                        self._active_node_widget = None

        return False

    def render_expression(self):
        self._active_node_widget = None
        self._selected_node_ids = set()
        self._node_widgets = {}
        while self.node_layout.count():
            item = self.node_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.node_layout.addStretch(1)
        for node in self.tree.get_expression():
            widget = self._create_node_widget(node)
            self._node_widgets[node.node_id] = widget
            widget.input_mode_requested.connect(self._on_input_mode_requested)
            widget.action_committed.connect(
                lambda action, payload, w=widget: self._on_action_committed(w, action, payload)
            )
            widget.selection_toggled.connect(self._on_selection_toggled)
            self.node_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.node_layout.addStretch(1)

    def _create_node_widget(self, node):
        if isinstance(node, OpNode):
            return OpNodeWidget(node.node_id, node.op_key)
        elif isinstance(node, IdNode):
            return IdNodeWidget(node.node_id, str(node))
        else:
            return ENodeWidget(node.node_id)

    def _on_selection_toggled(self, widget):
        if widget.is_selected():
            self._selected_node_ids.add(widget.node_id)
        else:
            self._selected_node_ids.discard(widget.node_id)

    def _clear_selection(self):
        for node_id in list(self._selected_node_ids):
            widget = self._node_widgets.get(node_id)
            if widget:
                widget.set_selected(False)
        self._selected_node_ids.clear()

    def _on_input_mode_requested(self, requesting_widget):
        self._clear_selection()
        if self._active_node_widget is not None and self._active_node_widget is not requesting_widget:
            self._active_node_widget.enter_display_mode()
        self._active_node_widget = requesting_widget
        if isinstance(requesting_widget, ENodeWidget):
            requesting_widget.set_variable_suggestions(
                self.proof_window.controller.get_used_variables()
            )
        requesting_widget.enter_input_mode()

    def _show_context_menu(self, global_pos):
        ancestor_id = self.tree.find_collapsible_ancestor(self._selected_node_ids)
        enabled = ancestor_id is not None
        menu = QMenu(self)

        collapse_action = menu.addAction("Réduire en E")
        collapse_action.setEnabled(enabled)
        if enabled:
            collapse_action.triggered.connect(
                lambda: self._on_collapse_to_enode(ancestor_id)
            )

        paren_action = menu.addAction("Mettre entre parenthèses")
        paren_action.setEnabled(enabled)
        if enabled:
            paren_action.triggered.connect(lambda: self._on_parenthesize(ancestor_id))

        annex_menu = menu.addMenu("Annexer →")
        annex_menu.setEnabled(enabled)
        if enabled:
            for op_key in _ANNEX_OPERATOR_ORDER:
                action = annex_menu.addAction(BooleanOperators[op_key].strip())
                action.triggered.connect(
                    lambda _, k=op_key, a=ancestor_id: self._on_annex_operator(a, k)
                )

        menu.exec(global_pos)

    def _on_collapse_to_enode(self, ancestor_id):
        self.proof_window.controller.collapse_subtree(self.expression_index, ancestor_id)

    def _on_parenthesize(self, ancestor_id):
        self.proof_window.controller.parenthesize(self.expression_index, ancestor_id)

    def _on_annex_operator(self, ancestor_id, op):
        self.proof_window.controller.annex_operator(self.expression_index, ancestor_id, op)

    def _on_action_committed(self, node_widget, action, payload):
        self._active_node_widget = None
        c = self.proof_window.controller
        idx = self.expression_index
        nid = node_widget.node_id

        if action == "expand":
            c.expand_node(idx, nid, payload)
        elif action == "to_id":
            c.convert_to_id(idx, nid, payload)
        elif action == "change_op":
            c.change_operator(idx, nid, payload)
        elif action == "rename":
            c.rename_id(idx, nid, payload)
        elif action == "revert":
            c.revert_to_enode(idx, nid)
