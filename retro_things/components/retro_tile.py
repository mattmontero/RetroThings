
import logging
from typing import Dict

from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QDialog
from PySide2 import QtCore
from app_manager import AppManager

class RetroDialog(QDialog):
    def __init__(self, label, owner, update_callback=None, *args, **kwargs):
        super(RetroDialog, self).__init__(*args, **kwargs)
        self.sid = owner.get("sid", "Unknown")
        self.owners_name = owner.get("name", "Unknown")
        self.update_callback = update_callback

        # Window Title
        self.setWindowTitle(self.owners_name)
        # Layout Data
        self.layout = QVBoxLayout()
        self.text_display = QTextEdit(label)
        self.update_button = QPushButton("Update")

        self._setup()

    def _setup(self):
        is_owner = self.sid == AppManager().sio.sid
        self.text_display.setReadOnly((not is_owner))
        self.layout.addWidget(self.text_display)
        if is_owner:
            self.layout.addWidget(self.update_button)
            self.update_button.clicked.connect(self.update_submission)
        self.setLayout(self.layout)

    def update_submission(self):
        text = self.text_display.toPlainText()
        self.update_callback(self.text_display.toPlainText())


class RetroTile(QWidget):
    update_signal = QtCore.Signal(dict)
    def __init__(self, tile_data, *args, **kwargs):
        super(RetroTile, self).__init__(*args, **kwargs)
        self.layout = QHBoxLayout()
        self.label = QPushButton()
        self.owner = tile_data['owner']
        self._text = tile_data['response']
        self._id = tile_data.get("response_id", None)
        self._time = tile_data['time']
        self._setup()
    
    @property
    def id(self):
        return self._id

    def _setup(self):
        self.label.setFixedWidth(400)
        temp_text = self._text.replace("\n", " ")
        if len(self._text) > 50:
            self.label.setText(f"{temp_text[:57]}...")
        else:
            self.label.setText(temp_text)
        self.label.clicked.connect(self.show_all)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def show_all(self):
        text = RetroDialog(self._text, self.owner, self.wrap_update)
        text.exec_()
    
    def wrap_update(self, data=None):
        payload = {
            "user_response": data
        }
        if self._id:
            payload.update({"response_id": self._id})
        self.update_signal.emit(payload)

    def init_update(self, data):
        print("Just joined? Let's set up all the data we know about")
        pass

    def update(self, data):
        if self._time != data['time']:
            self._time = data['time']
            self._text = data['response']
            self.label.setText(self._text)
