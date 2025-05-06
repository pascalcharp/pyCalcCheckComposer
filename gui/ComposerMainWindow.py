from PyQt6.QtWidgets import QMainWindow


class ComposerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Composer")
