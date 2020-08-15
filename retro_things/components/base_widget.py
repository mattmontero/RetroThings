from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QRadioButton
from app_manager import AppManager
from components.radio_list import RadioList
from components.labled_text_box import LabelTextBox

class OverrideInheritedMethod(Exception):
    pass

class BaseWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)

    def init_update(self, data):
        raise OverrideInheritedMethod(f"Class {self} must override init_update")

    def update(self, data):
        raise OverrideInheritedMethod(f"Class {self} must override update")
