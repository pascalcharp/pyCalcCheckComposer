import sys
import unittest
from uuid import uuid4

from PyQt6.QtWidgets import QApplication
from gui.ENodeWidget import ENodeWidget, _ENODE_EXPANSIONS

_app = QApplication.instance() or QApplication(sys.argv)


class ENodeWidgetDisplayTests(unittest.TestCase):

    def setUp(self):
        self.widget = ENodeWidget(uuid4())

    def test_starts_in_display_mode(self):
        self.assertFalse(self.widget.is_in_input_mode())

    def test_display_button_emits_input_mode_requested(self):
        received = []
        self.widget.input_mode_requested.connect(lambda w: received.append(w))
        self.widget._display_widget.click()
        self.assertEqual(1, len(received))
        self.assertIs(self.widget, received[0])


class ENodeWidgetExpandTests(unittest.TestCase):

    def setUp(self):
        self.widget = ENodeWidget(uuid4())
        self.received = []
        self.widget.action_committed.connect(lambda a, p: self.received.append((a, p)))

    def test_all_operator_buttons_present(self):
        expected = {op_key for op_key, _ in _ENODE_EXPANSIONS}
        self.assertEqual(expected, set(self.widget._op_buttons.keys()))

    def test_operator_button_emits_expand_action(self):
        self.widget._op_buttons["AndOperator"].click()
        self.assertEqual(1, len(self.received))
        self.assertEqual(("expand", "AndOperator"), self.received[0])

    def test_each_operator_button_passes_correct_key(self):
        for op_key, _ in _ENODE_EXPANSIONS:
            received = []
            self.widget.action_committed.connect(lambda a, p: received.append((a, p)))
            self.widget._op_buttons[op_key].click()
            self.assertEqual("expand", received[-1][0])
            self.assertEqual(op_key, received[-1][1])

    def test_operator_action_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._op_buttons["OrOperator"].click()
        self.assertFalse(self.widget.is_in_input_mode())


class ENodeWidgetVariableTests(unittest.TestCase):

    def setUp(self):
        self.widget = ENodeWidget(uuid4())
        self.received = []
        self.widget.action_committed.connect(lambda a, p: self.received.append((a, p)))

    def test_confirm_button_emits_to_id(self):
        self.widget._var_input.setText("p")
        self.widget._var_confirm.click()
        self.assertEqual(1, len(self.received))
        self.assertEqual(("to_id", "p"), self.received[0])

    def test_enter_key_emits_to_id(self):
        self.widget._var_input.setText("q")
        self.widget._var_input.returnPressed.emit()
        self.assertEqual(1, len(self.received))
        self.assertEqual(("to_id", "q"), self.received[0])

    def test_whitespace_only_does_not_commit(self):
        self.widget._var_input.setText("   ")
        self.widget._var_confirm.click()
        self.assertEqual(0, len(self.received))

    def test_empty_string_does_not_commit(self):
        self.widget._var_input.setText("")
        self.widget._var_confirm.click()
        self.assertEqual(0, len(self.received))

    def test_input_cleared_after_commit(self):
        self.widget._var_input.setText("p")
        self.widget._var_confirm.click()
        self.assertEqual("", self.widget._var_input.text())

    def test_variable_action_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._var_input.setText("r")
        self.widget._var_confirm.click()
        self.assertFalse(self.widget.is_in_input_mode())

    def test_name_is_stripped_before_commit(self):
        self.widget._var_input.setText("  p  ")
        self.widget._var_confirm.click()
        self.assertEqual(("to_id", "p"), self.received[0])


if __name__ == '__main__':
    unittest.main()
