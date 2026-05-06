import sys
import unittest
from uuid import uuid4

from PyQt6.QtWidgets import QApplication, QPushButton
from gui.NodeWidget import NodeWidget

_app = QApplication.instance() or QApplication(sys.argv)


class _StubNodeWidget(NodeWidget):
    """Implémentation minimale pour tester la classe de base sans modèle."""

    def _build_display_widget(self):
        btn = QPushButton("display")
        btn.clicked.connect(self._request_input_mode)
        return btn

    def _build_input_widget(self):
        btn = QPushButton("input")
        btn.clicked.connect(lambda: self._commit_action("stub_action", "stub_payload"))
        return btn


class NodeWidgetModeTests(unittest.TestCase):

    def setUp(self):
        self.widget = _StubNodeWidget(uuid4())

    def test_starts_in_display_mode(self):
        self.assertFalse(self.widget.is_in_input_mode())

    def test_enter_input_mode(self):
        self.widget.enter_input_mode()
        self.assertTrue(self.widget.is_in_input_mode())

    def test_enter_display_mode_after_input(self):
        self.widget.enter_input_mode()
        self.widget.enter_display_mode()
        self.assertFalse(self.widget.is_in_input_mode())

    def test_node_id_stored(self):
        node_id = uuid4()
        w = _StubNodeWidget(node_id)
        self.assertEqual(node_id, w.node_id)


class NodeWidgetSignalTests(unittest.TestCase):

    def setUp(self):
        self.widget = _StubNodeWidget(uuid4())

    def test_request_input_mode_emits_signal_with_self(self):
        received = []
        self.widget.input_mode_requested.connect(lambda w: received.append(w))
        self.widget._request_input_mode()
        self.assertEqual(1, len(received))
        self.assertIs(self.widget, received[0])

    def test_commit_action_emits_signal(self):
        received = []
        self.widget.action_committed.connect(lambda a, p: received.append((a, p)))
        self.widget._commit_action("test_action", "test_payload")
        self.assertEqual(1, len(received))
        self.assertEqual(("test_action", "test_payload"), received[0])

    def test_commit_action_none_payload(self):
        received = []
        self.widget.action_committed.connect(lambda a, p: received.append((a, p)))
        self.widget._commit_action("revert")
        self.assertEqual(("revert", None), received[0])

    def test_commit_action_returns_to_display_mode(self):
        self.widget.enter_input_mode()
        self.widget._commit_action("test_action")
        self.assertFalse(self.widget.is_in_input_mode())

    def test_multiple_signals_independent(self):
        received_input = []
        received_action = []
        self.widget.input_mode_requested.connect(lambda w: received_input.append(w))
        self.widget.action_committed.connect(lambda a, p: received_action.append((a, p)))

        self.widget._request_input_mode()
        self.widget._commit_action("action_a", 42)
        self.widget._request_input_mode()

        self.assertEqual(2, len(received_input))
        self.assertEqual(1, len(received_action))


if __name__ == '__main__':
    unittest.main()
