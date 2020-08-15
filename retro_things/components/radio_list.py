from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QRadioButton
from app_manager import AppManager

class RadioList(QWidget):
    def __init__(self, orientation, labels, signal = None, *args, **kwargs):
        super(RadioList, self).__init__(*args, **kwargs)
        self.layout = QVBoxLayout() if orientation == "V" else QHBoxLayout()
        self.button_list = list()
        self.active = None
        self.signal = signal
        self._setup(labels)

    def init_update(self, data):
        pass

    def radio_switch(self, toggled):
      if toggled:
        for button in self.button_list:
          if button.isChecked():
            self.active = button.text()
            self.signal()
        print("Active:", self.active)

    def _setup(self, labels):
        for label in labels:
          radio = QRadioButton(label)
          radio.toggled.connect(self.radio_switch)
          self.button_list.append(radio)
          self.layout.addWidget(radio)
        self.setLayout(self.layout)

    def _send_text(self):
        # AppManager().sio.emit("submit", payload)
        print(f"Send text for text edit")

    def update(self, data):
        print(f"Updating {self} with data - {data}")
