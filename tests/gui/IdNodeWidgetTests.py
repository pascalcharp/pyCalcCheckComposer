import sys
import unittest
from uuid import uuid4

from PyQt6.QtWidgets import QApplication
from gui.IdNodeWidget import IdNodeWidget

_app = QApplication.instance() or QApplication(sys.argv)


class IdNodeWidgetDisplayTests(unittest.TestCase):

    def setUp(self):
        self.widget = IdNodeWidget(uuid4(), "p")

    def test_starts_in_display_mode(self):
        self.assertFalse(self.widget.is_in_input_mode())

    def test_display_button_shows_variable_name(self):
        self.assertEqual("p", self.widget._display_widget.text())

    def test_display_button_is_enabled(self):
        self.assertTrue(self.widget._display_widget.isEnabled())

    def test_display_button_emits_input_mode_requested(self):
        received = []
        self.widget.input_mode_requested.connect(lambda w: received.append(w))
        self.widget._display_widget.click()
        self.assertEqual(1, len(received))
        self.assertIs(self.widget, received[0])

    def test_display_label_reflects_constructor_name(self):
        w = IdNodeWidget(uuid4(), "myVar")
        self.assertEqual("myVar", w._display_widget.text())


class IdNodeWidgetRenameTests(unittest.TestCase):

    def setUp(self):
        self.widget = IdNodeWidget(uuid4(), "p")
        self.received = []
        self.widget.action_committed.connect(lambda a, p: self.received.append((a, p)))

    def test_name_input_prefilled_with_current_name(self):
        self.assertEqual("p", self.widget._name_input.text())

    def test_confirm_button_emits_rename(self):
        self.widget._name_input.setText("q")
        self.widget._rename_confirm.click()
        self.assertEqual(1, len(self.received))
        self.assertEqual(("rename", "q"), self.received[0])

    def test_enter_key_emits_rename(self):
        self.widget._name_input.setText("r")
        self.widget._name_input.returnPressed.emit()
        self.assertEqual(1, len(self.received))
        self.assertEqual(("rename", "r"), self.received[0])

    def test_rename_strips_whitespace(self):
        self.widget._name_input.setText("  q  ")
        self.widget._rename_confirm.click()
        self.assertEqual(("rename", "q"), self.received[0])

    def test_empty_string_does_not_commit(self):
        self.widget._name_input.setText("")
        self.widget._rename_confirm.click()
        self.assertEqual(0, len(self.received))

    def test_whitespace_only_does_not_commit(self):
        self.widget._name_input.setText("   ")
        self.widget._rename_confirm.click()
        self.assertEqual(0, len(self.received))

    def test_rename_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._name_input.setText("q")
        self.widget._rename_confirm.click()
        self.assertFalse(self.widget.is_in_input_mode())


class IdNodeWidgetRevertTests(unittest.TestCase):

    def setUp(self):
        self.widget = IdNodeWidget(uuid4(), "p")
        self.received = []
        self.widget.action_committed.connect(lambda a, p: self.received.append((a, p)))

    def test_revert_button_emits_revert_action(self):
        self.widget._revert_button.click()
        self.assertEqual(1, len(self.received))
        self.assertEqual("revert", self.received[0][0])

    def test_revert_payload_is_none(self):
        self.widget._revert_button.click()
        self.assertIsNone(self.received[0][1])

    def test_revert_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._revert_button.click()
        self.assertFalse(self.widget.is_in_input_mode())


class IdNodeWidgetCancelTests(unittest.TestCase):

    def setUp(self):
        self.widget = IdNodeWidget(uuid4(), "p")
        self.received = []
        self.widget.action_committed.connect(lambda a, p: self.received.append((a, p)))

    def test_cancel_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._cancel_button.click()
        self.assertFalse(self.widget.is_in_input_mode())

    def test_cancel_does_not_emit_action(self):
        self.widget.enter_input_mode()
        self.widget._cancel_button.click()
        self.assertEqual(0, len(self.received))


if __name__ == '__main__':
    unittest.main()
