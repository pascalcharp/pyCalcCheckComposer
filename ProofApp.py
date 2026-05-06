import sys

from PyQt6.QtWidgets import QApplication

from controllers.ProofController import ProofController
from gui.ProofWindow import ProofWindow


class ProofApp:
    def __init__(self):
        self._qt_app = QApplication(sys.argv)
        self._windows = []

    def open_proof_window(self):
        controller = ProofController()
        window = ProofWindow(controller)
        controller.proof_window = window
        self._windows.append((controller, window))
        window.show()

    def run(self):
        self.open_proof_window()
        sys.exit(self._qt_app.exec())


if __name__ == "__main__":
    ProofApp().run()
