import logging
import sys
from typing import List

import requests
import socketio
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit, QStyle
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout

from app_manager import AppManager
from store import create_store
from components.retro_widget import RetroWidget
from components.color_game import ColorGame
from components.sign_in import SignIn


if __name__ == "__main__":
    app_man = app = None
    try:
        app = QApplication(sys.argv)
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        app_man = AppManager()
        app_man.connect_qt(app, main_widget, main_layout)

        # Each "Component" will be treated as a view
        # Each view must be added to the app_man widgets

        # wid = ColorGame()
        # app_man.add_widget(wid, ['color_game'])

        rw = RetroWidget(app_man)
        app_man.add_widget(rw, ["retro"])

        # si = SignIn()
        # app_man.add_widget(si, [])

        app_man.run()
    except Exception as e:
        print(f"Exception - {e}")
        raise
    finally:
        if app_man:
            app_man.destroy()
        if app:
            app.quit()
