
import logging

from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit, QLineEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QRadioButton
from app_manager import AppManager


class LabelTextBox(QWidget):
    def __init__(self, label, orientation="V", read_only=True, line=False, *args, **kwargs):
        super(LabelTextBox, self).__init__(*args, **kwargs)
        self.layout = QVBoxLayout() if orientation == "V" else QHBoxLayout()
        self.label = QLabel(label)
        self.text_box = QLineEdit() if line else QTextEdit()
        self._read_only = read_only
        self._line_edit = line
        self._text = ""
        self._setup()

    def _setup(self):
        self.text_box.setReadOnly(self._read_only)
        if not self._line_edit:
            self.text_box.setFixedSize(400, 200)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_box)
        self.setLayout(self.layout)

    def text(self):
        return self.text_box.text()

    def set_text(self, text):
        self.text_box.setText(text)

    def init_update(self, data):
        print("Just joined? Let's set up all the data we know about")
        pass

    def update(self, data):
        print(f"Updating {self} with data - {data}")

    def setDisabled(self, disabled):
        self.text_box.setDisabled(disabled)

    def isEnabled(self):
        return self.text_box.isEnabled()