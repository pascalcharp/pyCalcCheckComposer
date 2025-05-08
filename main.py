import sys

from PyQt6.QtWidgets import QApplication
from Composer import Composer
from gui.ComposerMainWindow import ComposerMainWindow

def main():
    app = QApplication([])
    _ = Composer()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()