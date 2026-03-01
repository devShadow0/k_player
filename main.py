import sys
import os
from PySide6.QtWidgets import QApplication
from src.player import Player
from PySide6.QtGui import QIcon
from src.player_ui import PlayerUI

def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and PyInstaller) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    icon_path = resource_path("assets/logo_256.png")
    app.setWindowIcon(QIcon(icon_path))

    player_backend = Player()
    window = PlayerUI(player_backend)

    window.show()
    sys.exit(app.exec())