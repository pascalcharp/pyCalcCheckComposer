import sys
import unittest
from uuid import uuid4

from PyQt6.QtWidgets import QApplication
from gui.OpNodeWidget import OpNodeWidget, _BINARY_OPERATORS

_app = QApplication.instance() or QApplication(sys.argv)


class OpNodeWidgetBinaryDisplayTests(unittest.TestCase):

    def setUp(self):
        self.widget = OpNodeWidget(uuid4(), "AndOperator")

    def test_starts_in_display_mode(self):
        self.assertFalse(self.widget.is_in_input_mode())

    def test_display_button_is_enabled_for_binary(self):
        self.assertTrue(self.widget._display_widget.isEnabled())

    def test_display_button_shows_operator_lexeme(self):
        self.assertEqual("and", self.widget._display_widget.text())

    def test_display_button_emits_input_mode_requested(self):
        received = []
        self.widget.input_mode_requested.connect(lambda w: received.append(w))
        self.widget._display_widget.click()
        self.assertEqual(1, len(received))
        self.assertIs(self.widget, received[0])


class OpNodeWidgetNonBinaryDisplayTests(unittest.TestCase):

    def test_not_operator_display_is_disabled(self):
        w = OpNodeWidget(uuid4(), "NotOperator")
        self.assertFalse(w._display_widget.isEnabled())

    def test_leftparen_display_is_disabled(self):
        w = OpNodeWidget(uuid4(), "Leftparen")
        self.assertFalse(w._display_widget.isEnabled())

    def test_rightparen_display_is_disabled(self):
        w = OpNodeWidget(uuid4(), "Rightparen")
        self.assertFalse(w._display_widget.isEnabled())


class OpNodeWidgetInputTests(unittest.TestCase):

    def setUp(self):
        self.widget = OpNodeWidget(uuid4(), "AndOperator")
        self.received = []
        self.widget.action_committed.connect(lambda a, p: self.received.append((a, p)))

    def test_alt_buttons_exclude_current_operator(self):
        self.assertNotIn("AndOperator", self.widget._alt_buttons)

    def test_alt_buttons_contain_all_other_binary_operators(self):
        expected = _BINARY_OPERATORS - {"AndOperator"}
        self.assertEqual(expected, set(self.widget._alt_buttons.keys()))

    def test_alt_button_emits_change_op_action(self):
        self.widget._alt_buttons["OrOperator"].click()
        self.assertEqual(1, len(self.received))
        self.assertEqual(("change_op", "OrOperator"), self.received[0])

    def test_each_alt_button_passes_correct_key(self):
        for alt_key in _BINARY_OPERATORS - {"AndOperator"}:
            received = []
            self.widget.action_committed.connect(lambda a, p: received.append((a, p)))
            self.widget._alt_buttons[alt_key].click()
            self.assertEqual("change_op", received[-1][0])
            self.assertEqual(alt_key, received[-1][1])

    def test_alt_button_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._alt_buttons["OrOperator"].click()
        self.assertFalse(self.widget.is_in_input_mode())

    def test_cancel_button_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._cancel_button.click()
        self.assertFalse(self.widget.is_in_input_mode())

    def test_cancel_button_does_not_emit_action(self):
        self.widget.enter_input_mode()
        self.widget._cancel_button.click()
        self.assertEqual(0, len(self.received))


class OpNodeWidgetVariantTests(unittest.TestCase):
    """Vérifie le comportement pour différentes valeurs d'opérateur binaire initial."""

    def test_or_operator_excludes_or_from_alts(self):
        w = OpNodeWidget(uuid4(), "OrOperator")
        self.assertNotIn("OrOperator", w._alt_buttons)
        self.assertIn("AndOperator", w._alt_buttons)

    def test_display_label_matches_operator(self):
        from BooleanExpression.Node.OpNode import BooleanOperators
        for op_key in _BINARY_OPERATORS:
            w = OpNodeWidget(uuid4(), op_key)
            expected_label = BooleanOperators[op_key].strip()
            self.assertEqual(expected_label, w._display_widget.text())


if __name__ == '__main__':
    unittest.main()
