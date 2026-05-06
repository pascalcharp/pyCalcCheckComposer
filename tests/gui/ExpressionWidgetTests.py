import sys
import unittest
from uuid import UUID

from PyQt6.QtWidgets import QApplication
from BooleanExpression.ExpressionTree import BooleanExpressionTree
from gui.ExpressionWidget import ExpressionWidget
from gui.ENodeWidget import ENodeWidget
from gui.OpNodeWidget import OpNodeWidget
from gui.IdNodeWidget import IdNodeWidget

_app = QApplication.instance() or QApplication(sys.argv)


class _MockController:
    def __init__(self):
        self.calls = []

    def expand_node(self, idx, node_id, op):
        self.calls.append(("expand_node", idx, node_id, op))

    def convert_to_id(self, idx, node_id, name):
        self.calls.append(("convert_to_id", idx, node_id, name))

    def change_operator(self, idx, node_id, new_op):
        self.calls.append(("change_operator", idx, node_id, new_op))

    def rename_id(self, idx, node_id, name):
        self.calls.append(("rename_id", idx, node_id, name))

    def revert_to_enode(self, idx, node_id):
        self.calls.append(("revert_to_enode", idx, node_id))


class _MockProofWindow:
    def __init__(self):
        self.controller = _MockController()

    def update_expression_widget(self, idx):
        pass

    def display_error_message(self, msg):
        pass


def _widgets(ew):
    return [ew.node_layout.itemAt(i).widget() for i in range(ew.node_layout.count())]


class ExpressionWidgetRenderTests(unittest.TestCase):

    def test_initial_tree_renders_single_enode_widget(self):
        be = BooleanExpressionTree()
        ew = ExpressionWidget(be, _MockProofWindow(), 0)
        ws = _widgets(ew)
        self.assertEqual(1, len(ws))
        self.assertIsInstance(ws[0], ENodeWidget)

    def test_binary_expansion_renders_enode_op_enode(self):
        be = BooleanExpressionTree()
        be.generate_binary_operator_production(be.get_root_id(), "AndOperator")
        ew = ExpressionWidget(be, _MockProofWindow(), 0)
        ws = _widgets(ew)
        self.assertEqual(3, len(ws))
        self.assertIsInstance(ws[0], ENodeWidget)
        self.assertIsInstance(ws[1], OpNodeWidget)
        self.assertIsInstance(ws[2], ENodeWidget)

    def test_id_production_renders_idnode_widget(self):
        be = BooleanExpressionTree()
        be.generate_id_production(be.get_root_id(), "p")
        ew = ExpressionWidget(be, _MockProofWindow(), 0)
        ws = _widgets(ew)
        self.assertEqual(1, len(ws))
        self.assertIsInstance(ws[0], IdNodeWidget)

    def test_idnode_widget_shows_variable_name(self):
        be = BooleanExpressionTree()
        be.generate_id_production(be.get_root_id(), "myVar")
        ew = ExpressionWidget(be, _MockProofWindow(), 0)
        ws = _widgets(ew)
        self.assertEqual("myVar", ws[0]._display_widget.text())

    def test_opnode_widget_shows_operator_lexeme(self):
        be = BooleanExpressionTree()
        be.generate_binary_operator_production(be.get_root_id(), "OrOperator")
        ew = ExpressionWidget(be, _MockProofWindow(), 0)
        ws = _widgets(ew)
        self.assertEqual("or", ws[1]._display_widget.text())

    def test_rerender_updates_widget_count(self):
        be = BooleanExpressionTree()
        ew = ExpressionWidget(be, _MockProofWindow(), 0)
        self.assertEqual(1, ew.node_layout.count())
        be.generate_binary_operator_production(be.get_root_id(), "AndOperator")
        ew.render_expression()
        self.assertEqual(3, ew.node_layout.count())


class ExpressionWidgetInputModeTests(unittest.TestCase):

    def _make_binary_widget(self):
        be = BooleanExpressionTree()
        be.generate_binary_operator_production(be.get_root_id(), "AndOperator")
        ew = ExpressionWidget(be, _MockProofWindow(), 0)
        ws = _widgets(ew)
        return ew, ws[0], ws[2]  # ew, lhs ENodeWidget, rhs ENodeWidget

    def test_clicking_display_enters_input_mode(self):
        _, lhs, _ = self._make_binary_widget()
        lhs._display_widget.click()
        self.assertTrue(lhs.is_in_input_mode())

    def test_second_click_closes_first_node(self):
        _, lhs, rhs = self._make_binary_widget()
        lhs._display_widget.click()
        rhs._display_widget.click()
        self.assertTrue(rhs.is_in_input_mode())
        self.assertFalse(lhs.is_in_input_mode())

    def test_active_widget_tracked(self):
        ew, lhs, _ = self._make_binary_widget()
        lhs._display_widget.click()
        self.assertIs(lhs, ew._active_node_widget)

    def test_active_widget_cleared_on_rerender(self):
        ew, lhs, _ = self._make_binary_widget()
        lhs._display_widget.click()
        ew.render_expression()
        self.assertIsNone(ew._active_node_widget)


class ExpressionWidgetRoutingTests(unittest.TestCase):

    def _make(self, tree):
        mock = _MockProofWindow()
        ew = ExpressionWidget(tree, mock, 2)  # index 2 pour vérifier la propagation
        return ew, mock.controller, _widgets(ew)

    def test_expand_routes_to_controller(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        ew, ctrl, ws = self._make(be)
        ws[0]._op_buttons["AndOperator"].click()
        self.assertEqual(1, len(ctrl.calls))
        name, idx, nid, op = ctrl.calls[0]
        self.assertEqual("expand_node", name)
        self.assertEqual(2, idx)
        self.assertEqual(root_id, nid)
        self.assertEqual("AndOperator", op)

    def test_to_id_routes_to_controller(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        ew, ctrl, ws = self._make(be)
        ws[0]._var_input.setText("p")
        ws[0]._var_confirm.click()
        name, idx, nid, var = ctrl.calls[0]
        self.assertEqual("convert_to_id", name)
        self.assertEqual(2, idx)
        self.assertEqual(root_id, nid)
        self.assertEqual("p", var)

    def test_change_op_routes_to_controller(self):
        be = BooleanExpressionTree()
        be.generate_binary_operator_production(be.get_root_id(), "AndOperator")
        ew, ctrl, ws = self._make(be)
        op_widget = ws[1]  # OpNodeWidget
        op_widget._alt_buttons["OrOperator"].click()
        name, idx, nid, new_op = ctrl.calls[0]
        self.assertEqual("change_operator", name)
        self.assertEqual(2, idx)
        self.assertEqual("OrOperator", new_op)

    def test_rename_routes_to_controller(self):
        be = BooleanExpressionTree()
        be.generate_id_production(be.get_root_id(), "p")
        ew, ctrl, ws = self._make(be)
        id_widget = ws[0]  # IdNodeWidget
        id_widget._name_input.setText("q")
        id_widget._rename_confirm.click()
        name, idx, nid, new_name = ctrl.calls[0]
        self.assertEqual("rename_id", name)
        self.assertEqual(2, idx)
        self.assertEqual("q", new_name)

    def test_revert_routes_to_controller(self):
        be = BooleanExpressionTree()
        be.generate_id_production(be.get_root_id(), "p")
        ew, ctrl, ws = self._make(be)
        id_widget = ws[0]  # IdNodeWidget
        id_widget._revert_button.click()
        name, idx, nid = ctrl.calls[0]
        self.assertEqual("revert_to_enode", name)
        self.assertEqual(2, idx)

    def test_action_clears_active_node_widget(self):
        be = BooleanExpressionTree()
        root_id = be.get_root_id()
        ew, ctrl, ws = self._make(be)
        ws[0]._display_widget.click()
        self.assertIsNotNone(ew._active_node_widget)
        ws[0]._op_buttons["AndOperator"].click()
        self.assertIsNone(ew._active_node_widget)


if __name__ == '__main__':
    unittest.main()
