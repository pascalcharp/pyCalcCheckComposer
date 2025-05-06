import sys

from PyQt6.QtWidgets import QApplication
from Composer import Composer
from gui.ComposerMainWindow import ComposerMainWindow

def main():
    app = QApplication([])
    window = ComposerMainWindow()
    composer = Composer(window)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()