import Node.ENode
import Node.IdNode
from BooleanExpression.Node.ENode import ENode
from BooleanExpression.Node.OpNode import OpNode
import Node.NonTerminalNode


class BooleanExpression:
    def __init__(self):
        self._root_node = Node.ENode.ENode()
        self._nodes = {self._root_node.node_id: self._root_node}

    def get_root_id(self):
        return self._root_node.node_id

    def get_node(self, node_id):
        return self._nodes[node_id]

    def aux_collapse_node(self, node):
        if not node.has_children():
            return

        for child in node.get_children():
            self.aux_collapse_node(child)
            self._nodes.pop(child.node_id)

        node.clear_children()

    def collapse_node(self, node_id):
        node = self._nodes[node_id]
        if not node.has_children():
            raise Exception('Node {} has no children'.format(node_id))
        self.aux_collapse_node(node)

    def generate_id_production(self, node_id, name):
        node = self._nodes[node_id]
        assert(isinstance(node, Node.ENode.ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        new_node = Node.IdNode.IdNode(name)
        node.add_children([new_node])
        self._nodes.update({new_node.node_id, new_node})

        return new_node.node_id

    def generate_binary_operator_production(self, node_id, op):
        node = self._nodes[node_id]
        assert(isinstance(node, Node.ENode.ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        lhs = ENode()
        rhs = ENode()
        node.add_children([lhs, OpNode(op), rhs])
        self._nodes.update({lhs.node_id: lhs, rhs.node_id: rhs})
        return lhs.node_id, rhs.node_id

    def generate_unary_operator_production(self, node_id, op):
        node = self._nodes[node_id]
        assert(isinstance(node, Node.ENode.ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        arg = ENode()
        node.add_children([OpNode(op), arg])
        self._nodes.update({arg.node_id: arg})
        return arg.node_id

    def generate_parenthesis_production(self, node_id):
        node = self._nodes[node_id]
        assert(isinstance(node, Node.ENode.ENode))
        if node.has_children():
            raise Exception('Node {} may not be expanded'.format(node_id))

        arg = ENode()
        node.add_children([OpNode("Leftparen"), arg, OpNode("Rightparen")])
        self._nodes.update({arg.node_id: arg})
        return arg.node_id

    def modify_id_name(self, node_id, name):
        node = self._nodes[node_id]
        assert(isinstance(node, Node.IdNode.IdNode))

        node.substitute_lexeme(name)

    def aux_build_output_string(self, node, string_value):
        if not node.has_children():
            string_value += node.__str__()
        else:
            for child in node.get_children():
                string_value += self.aux_build_output_string(child, string_value)
        return string_value

    def __str__(self):
        return self.aux_build_output_string(self._root_node, "")