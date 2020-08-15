from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
from app_manager import AppManager
from components.radio_list import RadioList
from components.labled_text_box import LabelTextBox
from components.base_widget import BaseWidget

class SignIn(BaseWidget):
    def __init__(self, *args, **kwargs):
        super(SignIn, self).__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.label = QLabel("Who are you?")
        self.input = QLineEdit()
        self.submit_button = QPushButton("Join")
        self._setup()

    def update(self, data):
        print(f"Updating {self} with data - {data}")

    def init_update(self, data):
        print("data", data)

    def _setup(self):
        self.submit_button.setEnabled(False)
        self.input.textChanged.connect(self.input_changed)
        self.submit_button.clicked.connect(self.join)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def input_changed(self, data):
        if data:
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def join(self):
        print(f"Joining - {self.input.text()}")
