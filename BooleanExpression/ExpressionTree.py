
from BooleanExpression.Node.ENode import ENode
from BooleanExpression.Node.OpNode import OpNode
from BooleanExpression.Node.IdNode import IdNode



class BooleanExpressionTree:
    def __init__(self):
        self._root_node = ENode()
        self._nodes = {self._root_node.node_id: self._root_node}
        self._parents = {}

    def get_root_id(self):
        return self._root_node.node_id

    def get_node(self, node_id):
        return self._nodes[node_id]

    def get_parent_id(self, node_id):
        return self._parents[node_id]

    def aux_collapse_node(self, node):
        if not node.has_children():
            return

        for child in node.get_children():
            self.aux_collapse_node(child)
            self._nodes.pop(child.node_id)
            self._parents.pop(child.node_id, None)

        node.clear_children()

    def collapse_node(self, node_id):
        node = self._nodes[node_id]
        if not node.has_children():
            raise Exception('Node {} has no children'.format(node_id))
        self.aux_collapse_node(node)

    def generate_id_production(self, node_id, name):
        node = self._nodes[node_id]
        assert(isinstance(node, ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        new_node = IdNode(name)
        node.add_children([new_node])
        self._nodes[new_node.node_id] = new_node
        self._parents[new_node.node_id] = node_id

        return new_node.node_id

    def generate_binary_operator_production(self, node_id, op):
        node = self._nodes[node_id]
        assert(isinstance(node, ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        lhs = ENode()
        op_node = OpNode(op)
        rhs = ENode()
        node.add_children([lhs, op_node, rhs])
        self._nodes.update({lhs.node_id: lhs, op_node.node_id: op_node, rhs.node_id: rhs})
        self._parents.update({lhs.node_id: node_id, op_node.node_id: node_id, rhs.node_id: node_id})
        return lhs.node_id, rhs.node_id

    def generate_unary_operator_production(self, node_id, op):
        node = self._nodes[node_id]
        assert(isinstance(node, ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        op_node = OpNode(op)
        arg = ENode()
        node.add_children([op_node, arg])
        self._nodes.update({op_node.node_id: op_node, arg.node_id: arg})
        self._parents.update({op_node.node_id: node_id, arg.node_id: node_id})
        return arg.node_id

    def generate_parenthesis_production(self, node_id):
        node = self._nodes[node_id]
        assert(isinstance(node, ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        lp = OpNode("Leftparen")
        arg = ENode()
        rp = OpNode("Rightparen")
        node.add_children([lp, arg, rp])
        self._nodes.update({lp.node_id: lp, arg.node_id: arg, rp.node_id: rp})
        self._parents.update({lp.node_id: node_id, arg.node_id: node_id, rp.node_id: node_id})
        return arg.node_id

    def change_operator(self, op_node_id, new_op):
        node = self._nodes[op_node_id]
        assert isinstance(node, OpNode)
        node.substitute_operator(new_op)

    def revert_id_to_enode(self, id_node_id):
        parent_id = self._parents[id_node_id]
        self.collapse_node(parent_id)

    def modify_id_name(self, node_id, name):
        node = self._nodes[node_id]
        assert(isinstance(node, IdNode))

        node.substitute_lexeme(name)

    def aux_build_output_string(self, node, string_value):
        if not node.has_children():
            string_value += node.__str__()
        else:
            for child in node.get_children():
                string_value = self.aux_build_output_string(child, string_value)
        return string_value

    def aux_build_expression(self, node, expression):
        if not node.has_children():
            expression.append(node)
        else:
            for child in node.get_children():
                self.aux_build_expression(child, expression)

    def get_expression(self):
        expression = []
        self.aux_build_expression(self._root_node, expression)
        return expression

    def find_collapsible_ancestor(self, node_ids: set):
        """
        Retourne l'id de l'ENode ancêtre minimal dont l'ensemble exact de feuilles == node_ids,
        ou None si aucun tel ancêtre n'existe.
        """
        if not node_ids:
            return None

        def get_ancestors(nid):
            ancestors = []
            current = nid
            while current in self._parents:
                current = self._parents[current]
                ancestors.append(current)
            return ancestors  # du parent immédiat jusqu'à la racine

        chains = [get_ancestors(nid) for nid in node_ids]

        common = set(chains[0])
        for chain in chains[1:]:
            common &= set(chain)

        if not common:
            return None

        # Le LCA est le premier ancêtre du premier nœud qui est commun à tous.
        for candidate in chains[0]:
            if candidate in common:
                leaves = []
                self.aux_build_expression(self._nodes[candidate], leaves)
                if {n.node_id for n in leaves} == node_ids:
                    return candidate
                return None  # LCA trouvé mais ne couvre pas exactement la sélection

        return None

    def __str__(self):
        return self.aux_build_output_string(self._root_node, "")
