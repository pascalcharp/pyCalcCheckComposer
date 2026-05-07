import unittest
from BooleanExpression.ExpressionTree import BooleanExpressionTree
from BooleanExpression.Node.ENode import ENode
from BooleanExpression.Node.OpNode import OpNode, BooleanOperators
from BooleanExpression.Node.IdNode import IdNode


class OpNodeSubstituteOperatorTests(unittest.TestCase):

    def test_substitute_binary_operator(self):
        node = OpNode("AndOperator")
        node.substitute_operator("OrOperator")
        self.assertEqual(BooleanOperators["OrOperator"], str(node))

    def test_substitute_does_not_affect_other_instances(self):
        n1 = OpNode("AndOperator")
        n2 = OpNode("AndOperator")
        n1.substitute_operator("OrOperator")
        self.assertEqual(BooleanOperators["AndOperator"], str(n2))

    def test_substitute_invalid_operator_raises(self):
        node = OpNode("AndOperator")
        with self.assertRaises(KeyError):
            node.substitute_operator("BogusOperator")


class ParentTrackingTests(unittest.TestCase):

    def test_id_production_parent(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        id_node_id = be.generate_id_production(root_id, "p")
        self.assertEqual(root_id, be.get_parent_id(id_node_id))

    def test_binary_production_parents(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        self.assertEqual(root_id, be.get_parent_id(lhs_id))
        self.assertEqual(root_id, be.get_parent_id(rhs_id))

    def test_binary_production_opnode_parent(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        be.generate_binary_operator_production(root_id, "AndOperator")
        nodes = be.get_expression()
        op_node = next(n for n in nodes if isinstance(n, OpNode))
        self.assertEqual(root_id, be.get_parent_id(op_node.node_id))

    def test_unary_production_parents(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        arg_id = be.generate_unary_operator_production(root_id, "NotOperator")
        self.assertEqual(root_id, be.get_parent_id(arg_id))
        nodes = be.get_expression()
        op_node = next(n for n in nodes if isinstance(n, OpNode))
        self.assertEqual(root_id, be.get_parent_id(op_node.node_id))

    def test_parenthesis_production_parents(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        arg_id = be.generate_parenthesis_production(root_id)
        self.assertEqual(root_id, be.get_parent_id(arg_id))

    def test_root_has_no_parent(self):
        be = BooleanExpressionTree()
        with self.assertRaises(KeyError):
            be.get_parent_id(be.get_root_id())


class ChangeOperatorTests(unittest.TestCase):

    def test_change_binary_operator(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        be.generate_binary_operator_production(root_id, "AndOperator")
        nodes = be.get_expression()
        op_node = next(n for n in nodes if isinstance(n, OpNode))
        be.change_operator(op_node.node_id, "OrOperator")
        self.assertIn(BooleanOperators["OrOperator"], str(be))
        self.assertNotIn(BooleanOperators["AndOperator"], str(be))

    def test_change_operator_preserves_structure(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        be.generate_id_production(lhs_id, "p")
        be.generate_id_production(rhs_id, "q")
        nodes = be.get_expression()
        op_node = next(n for n in nodes if isinstance(n, OpNode))
        be.change_operator(op_node.node_id, "OrOperator")
        expected = f"p{BooleanOperators['OrOperator']}q"
        self.assertEqual(expected, str(be))


class RevertIdToEnodeTests(unittest.TestCase):

    def test_revert_restores_enode(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        id_node_id = be.generate_id_production(root_id, "p")
        be.revert_id_to_enode(id_node_id)
        self.assertEqual("E", str(be))

    def test_revert_enode_is_expandable_again(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        id_node_id = be.generate_id_production(root_id, "p")
        be.revert_id_to_enode(id_node_id)
        be.generate_id_production(be.get_root_id(), "q")
        self.assertEqual("q", str(be))

    def test_revert_cleans_up_nodes(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        id_node_id = be.generate_id_production(root_id, "p")
        be.revert_id_to_enode(id_node_id)
        with self.assertRaises(KeyError):
            be.get_node(id_node_id)

    def test_revert_cleans_up_parents(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        id_node_id = be.generate_id_production(root_id, "p")
        be.revert_id_to_enode(id_node_id)
        with self.assertRaises(KeyError):
            be.get_parent_id(id_node_id)


class FindCollapsibleAncestorTests(unittest.TestCase):

    def _leaf_ids_of(self, be, node_id):
        leaves = []
        be.aux_build_expression(be.get_node(node_id), leaves)
        return {n.node_id for n in leaves}

    def test_empty_selection_returns_none(self):
        be = BooleanExpressionTree()
        self.assertIsNone(be.find_collapsible_ancestor(set()))

    def test_all_leaves_flat_tree_returns_root(self):
        # E0 → [E1→p, AND, E2→q]
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        be.generate_id_production(lhs_id, "p")
        be.generate_id_production(rhs_id, "q")
        all_ids = {n.node_id for n in be.get_expression()}
        self.assertEqual(root_id, be.find_collapsible_ancestor(all_ids))

    def test_partial_flat_selection_returns_none(self):
        # E0 → [E1→p, AND, E2→q]; sélection incomplète
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        be.generate_id_production(lhs_id, "p")
        be.generate_id_production(rhs_id, "q")
        leaves = be.get_expression()
        partial_ids = {n.node_id for n in leaves[:-1]}
        self.assertIsNone(be.find_collapsible_ancestor(partial_ids))

    def test_subtree_leaves_returns_subtree_root(self):
        # E0 → [E1→p, AND, E2 → [E3→q, OR, E4→r]]; sélection des feuilles de E2
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        be.generate_id_production(lhs_id, "p")
        q_id, r_id = be.generate_binary_operator_production(rhs_id, "OrOperator")
        be.generate_id_production(q_id, "q")
        be.generate_id_production(r_id, "r")
        rhs_leaf_ids = self._leaf_ids_of(be, rhs_id)
        self.assertEqual(rhs_id, be.find_collapsible_ancestor(rhs_leaf_ids))

    def test_all_leaves_nested_tree_returns_root(self):
        # Même arbre; sélection de toutes les feuilles → racine
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        be.generate_id_production(lhs_id, "p")
        q_id, r_id = be.generate_binary_operator_production(rhs_id, "OrOperator")
        be.generate_id_production(q_id, "q")
        be.generate_id_production(r_id, "r")
        all_ids = {n.node_id for n in be.get_expression()}
        self.assertEqual(root_id, be.find_collapsible_ancestor(all_ids))

    def test_cross_subtree_missing_operator_returns_none(self):
        # E0 → [E1→p, AND, E2 → [E3→q, OR, E4→r]]; p+q+OR+r sans le AND
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        be.generate_id_production(lhs_id, "p")
        q_id, r_id = be.generate_binary_operator_production(rhs_id, "OrOperator")
        be.generate_id_production(q_id, "q")
        be.generate_id_production(r_id, "r")
        cross_ids = self._leaf_ids_of(be, lhs_id) | self._leaf_ids_of(be, rhs_id)
        self.assertIsNone(be.find_collapsible_ancestor(cross_ids))

    def test_single_id_node_returns_parent_enode(self):
        # E0 → [E1→p, AND, E2→q]; sélection de {p} → E1
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        lhs_id, rhs_id = be.generate_binary_operator_production(root_id, "AndOperator")
        p_id = be.generate_id_production(lhs_id, "p")
        be.generate_id_production(rhs_id, "q")
        self.assertEqual(lhs_id, be.find_collapsible_ancestor({p_id}))


if __name__ == '__main__':
    unittest.main()
