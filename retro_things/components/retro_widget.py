from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QRadioButton
from app_manager import AppManager
from components.radio_list import RadioList
from components.labled_text_box import LabelTextBox
from components.base_widget import BaseWidget

class RetroWidget(BaseWidget):
    def __init__(self, app_man, *args, **kwargs):
        super(RetroWidget, self).__init__(*args, **kwargs)
        self.app_man = app_man
        self.layout = QVBoxLayout()

        self.name_row = QHBoxLayout()

        ##### Everything we need for display boxes #####
        self.row_one = QHBoxLayout()
        self.row_two = QHBoxLayout()
        self.submit_row = QVBoxLayout()
        self.display_boxes = dict()

        self.categories = [
            "What went well?",
            "What did not go well?",
            "Share something we should start doing.",
            "Hate it? Want to stop doing something?"
        ]

        for category in self.categories:
            self.display_boxes.update({category: LabelTextBox(category)})
        ##### Done with display boxes #####

        ##### Evertyhing to setting up the name ####
        self.name = LabelTextBox("Name:", orientation="H", read_only=False, line=True)
        self.set_name_button = QPushButton("Set Name")
        ##### Done with name boxes #####

        ##### Everything we need for submit box #####
        self.radio_list = RadioList('H', self.categories, self.radio_signal)
        self.text_edit = QTextEdit("Enter text")
        self.submit_button = QPushButton("Submit")
        ##### Done with submit box #####

        self._setup()
        self.submit_button.clicked.connect(self._send_text)
        self.app_man.emit("retro", {"event": "join"})

    def radio_signal(self):
        if not self.name.isEnabled():
            self.submit_button.setEnabled(True)

    def update(self, data):
        category_answers = data["category_answers"]
        for key in category_answers:
            formatted_text = '\n'.join(category_answers[key])
            self.display_boxes[key].set_text(formatted_text)

    def init_update(self, data):
        pass

    def _setup(self):
        self.submit_button.setEnabled(False)
        self.set_name_button.clicked.connect(self.set_name)

        self.name_row.addWidget(self.name)
        self.name_row.addWidget(self.set_name_button)

        self.row_one.addWidget(self.display_boxes[self.categories[0]])
        self.row_one.addWidget(self.display_boxes[self.categories[1]])
        self.row_two.addWidget(self.display_boxes[self.categories[2]])
        self.row_two.addWidget(self.display_boxes[self.categories[3]])

        self.submit_row.addWidget(self.radio_list)
        self.submit_row.addWidget(self.text_edit)
        self.submit_row.addWidget(self.submit_button)

        self.layout.addLayout(self.name_row)
        self.layout.addLayout(self.row_one)
        self.layout.addLayout(self.row_two)
        self.layout.addLayout(self.submit_row)

        self.setLayout(self.layout)

    def set_name(self):
        if self.name.isEnabled():
            if len(self.name.text()) == 0:
                print("Enter a name!")
                return
            self.name.setDisabled(True)
            self.set_name_button.setDisabled(True)
            name_payload = {
                "event": "join",
                "name": self.name.text()
            }
            self.app_man.emit("retro", name_payload)
            self.row_one.setEnabled(True)
            self.row_two.setEnabled(True)
            self.submit_row.setEnabled(True)

    def _send_text(self):
        if len(self.text_edit.toPlainText()) == 0:
            return
        payload = {
            "event": "submission",
            "category": self.radio_list.active,
            "user_response": self.text_edit.toPlainText()
        }
        self.app_man.emit("retro", payload)
