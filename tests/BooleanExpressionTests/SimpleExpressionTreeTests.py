import unittest
from BooleanExpression.ExpressionTree import BooleanExpressionTree
from BooleanExpression.Node.ENode import ENode
from BooleanExpression.Node.OpNode import OpNode


class ExpressionTreeTests(unittest.TestCase):
    def sequence_to_string(self, seq):
        retval = ""
        for node in seq:
            retval += node.__str__()
        return retval

    def test_starting_tree(self):
        be = BooleanExpressionTree()
        self.assertEqual("E", be.__str__())
        node_sequence = be.get_expression()
        self.assertEqual("E", self.sequence_to_string(node_sequence))

    def test_expand_root_node_with_id_production(self):
        be = BooleanExpressionTree()
        rnid = be.get_root_id()
        be.generate_id_production(rnid, "p")
        self.assertEqual("p", be.__str__())
        node_sequence = be.get_expression()
        self.assertEqual("p", self.sequence_to_string(node_sequence))

    def test_expand_root_node_with_binary_operator(self):
        be = BooleanExpressionTree()
        rnid = be.get_root_id()
        be.generate_binary_operator_production(rnid, "AndOperator")
        expected_string = ENode().__str__() + OpNode("AndOperator").__str__() + ENode().__str__()
        self.assertEqual(expected_string, be.__str__())
        node_sequence = be.get_expression()
        self.assertEqual(expected_string, self.sequence_to_string(node_sequence))

    def test_expand_root_node_with_multiple_operators(self):
        be = BooleanExpressionTree()
        rnid = be.get_root_id()
        lhs, rhs = be.generate_binary_operator_production(rnid, "AndOperator")
        arg = be.generate_parenthesis_production(lhs)
        be.generate_binary_operator_production(arg, "OrOperator")
        expected_string = f"{OpNode('Leftparen')}{ENode()}{OpNode('OrOperator')}{ENode()}{OpNode('Rightparen')}{OpNode('AndOperator')}{ENode()}"
        self.assertEqual(expected_string, be.__str__())
        node_sequence = be.get_expression()
        self.assertEqual(expected_string, self.sequence_to_string(node_sequence))

if __name__ == '__main__':
    unittest.main()
