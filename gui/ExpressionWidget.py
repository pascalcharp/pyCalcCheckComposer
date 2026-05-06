from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

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

        self.node_layout = QHBoxLayout()
        self.render_expression()
        self.setLayout(self.node_layout)

    def render_expression(self):
        self._active_node_widget = None
        while self.node_layout.count():
            item = self.node_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.node_layout.addStretch(1)
        for node in self.tree.get_expression():
            widget = self._create_node_widget(node)
            widget.input_mode_requested.connect(self._on_input_mode_requested)
            widget.action_committed.connect(
                lambda action, payload, w=widget: self._on_action_committed(w, action, payload)
            )
            self.node_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.node_layout.addStretch(1)

    def _create_node_widget(self, node):
        if isinstance(node, OpNode):
            return OpNodeWidget(node.node_id, node.op_key)
        elif isinstance(node, IdNode):
            return IdNodeWidget(node.node_id, str(node))
        else:
            return ENodeWidget(node.node_id)

    def _on_input_mode_requested(self, requesting_widget):
        if self._active_node_widget is not None and self._active_node_widget is not requesting_widget:
            self._active_node_widget.enter_display_mode()
        self._active_node_widget = requesting_widget
        requesting_widget.enter_input_mode()

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
