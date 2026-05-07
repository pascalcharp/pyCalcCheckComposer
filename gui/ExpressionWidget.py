from PyQt6.QtWidgets import QWidget, QHBoxLayout, QApplication, QMenu
from PyQt6.QtCore import Qt, QEvent

from BooleanExpression.Node.IdNode import IdNode
from BooleanExpression.Node.OpNode import OpNode
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
        requesting_widget.enter_input_mode()

    def _show_context_menu(self, global_pos):
        ancestor_id = self.tree.find_collapsible_ancestor(self._selected_node_ids)
        menu = QMenu(self)
        collapse_action = menu.addAction("Réduire en E")
        collapse_action.setEnabled(ancestor_id is not None)
        if menu.exec(global_pos) == collapse_action and ancestor_id is not None:
            self._on_collapse_to_enode(ancestor_id)

    def _on_collapse_to_enode(self, ancestor_id):
        self.proof_window.controller.collapse_subtree(self.expression_index, ancestor_id)

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
