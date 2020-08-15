from PySide2.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from components.base_widget import BaseWidget
from app_manager import AppManager

class ColorGame(BaseWidget):
    user_color_text = "Your Color: {color}"
    def __init__(self, *args, **kwargs):
        super(ColorGame, self).__init__(*args, **kwargs)
        self.layout =  QVBoxLayout()
        self.user_color = None
        self.username = "Matt"
        self.label = QLabel(f"Current Color: {self.user_color}")
        self.submit = QPushButton()
        self._setup()
        self.submit.clicked.connect(self._send)

    def _send(self):
        if self.username:
            payload = { "user": self.username, "color_submit": self.user_color}
            AppManager().sio.emit("color_game", payload)

    def _setup(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.submit)
        self.submit.setStyleSheet("width: 200px; height: 200px")
        self.setLayout(self.layout)

    def init_update(self, server_data):
        color_game_data = server_data['color_game']
        user_data = server_data['users'][AppManager().sio.sid]
        self._set_user_color(user_data.get('color', None))

        color = color_game_data.get("current_color", None)
        print("Current color:", color)
        if color:
            self._set_current_color(color)
    
    def _set_current_color(self, color):
        self.label.setText(f"Current Color: {color}")

    def _set_user_color(self, color):
        if not color:
            print("NO COLOR")
            return
        self.user_color = color
        self.submit.setStyleSheet(f"background: {color}; width: 200px; height: 200px")

    def update(self, data):
        print("Update data", data)
        color_game_data = data["server"]["color_game"]

        winner = color_game_data.get("winner", None)
        if winner:
            self.label.setText(f"Game Over: {winner}")
            self.submit.setDisabled(True)
            return

        color = color_game_data.get("current_color", None)
        print("Current color:", color)
        if color:
            self._set_current_color(color)
