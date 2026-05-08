from BooleanExpression.ExpressionTree import BooleanExpressionTree
from BooleanExpression.Node.IdNode import IdNode
from gui.ExpressionWidget import ExpressionWidget

_DEFAULT_VARIABLES = ["p", "q", "r", "s", "t"]


class ProofController:
    def __init__(self):
        self.proof_window = None
        self.proofs = []

    def add_new_expression(self):
        new_expression_tree = BooleanExpressionTree()
        self.proofs.append(new_expression_tree)
        expression_index = len(self.proofs) - 1
        new_expression_widget = ExpressionWidget(new_expression_tree, self.proof_window, expression_index)
        self.proof_window.add_expression_widget(new_expression_widget)

    def expand_node(self, expression_index, node_id, operator):
        tree = self.proofs[expression_index]
        def do():
            if operator == "NotOperator":
                tree.generate_unary_operator_production(node_id, operator)
            elif operator == "Leftparen":
                tree.generate_parenthesis_production(node_id)
            else:
                tree.generate_binary_operator_production(node_id, operator)
        self._refresh(expression_index, do)

    def convert_to_id(self, expression_index, enode_id, name):
        tree = self.proofs[expression_index]
        self._refresh(expression_index, lambda: tree.generate_id_production(enode_id, name))

    def change_operator(self, expression_index, op_node_id, new_op):
        tree = self.proofs[expression_index]
        self._refresh(expression_index, lambda: tree.change_operator(op_node_id, new_op))

    def rename_id(self, expression_index, id_node_id, new_name):
        tree = self.proofs[expression_index]
        self._refresh(expression_index, lambda: tree.modify_id_name(id_node_id, new_name))

    def revert_to_enode(self, expression_index, id_node_id):
        tree = self.proofs[expression_index]
        self._refresh(expression_index, lambda: tree.revert_id_to_enode(id_node_id))

    def collapse_subtree(self, expression_index, enode_id):
        tree = self.proofs[expression_index]
        self._refresh(expression_index, lambda: tree.collapse_node(enode_id))

    def annex_operator(self, expression_index, ancestor_id, op):
        tree = self.proofs[expression_index]
        self._refresh(expression_index, lambda: tree.annex_operator(ancestor_id, op))

    def get_used_variables(self) -> list[str]:
        seen = set()
        names = []
        for tree in self.proofs:
            for node in tree.get_expression():
                if isinstance(node, IdNode) and str(node) not in seen:
                    seen.add(str(node))
                    names.append(str(node))
        return names if names else list(_DEFAULT_VARIABLES)

    def _refresh(self, expression_index, operation):
        try:
            operation()
            self.proof_window.update_expression_widget(expression_index)
        except Exception as e:
            self.proof_window.display_error_message(str(e))
