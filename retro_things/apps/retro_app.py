from typing import Dict

from PySide2.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QRadioButton
from app_manager import AppManager
from components.labled_text_box import LabelTextBox
from components.radio_list import RadioList
from components.retro_box import RetroBox
from components.base_widget import BaseWidget

class RetroModel:
    def __init__(self, user):
        self.user = user

class RetroApp(BaseWidget):
    def __init__(self, app_man, *args, **kwargs):
        super(RetroApp, self).__init__(*args, **kwargs)
        self.app_man = app_man
        self.layout = QVBoxLayout()

        self.name_row = QHBoxLayout()

        ##### Everything we need for display boxes #####
        self.row_one = QHBoxLayout()
        self.row_two = QHBoxLayout()
        self.display_boxes = dict()

        self.categories = [
            "What went well?",
            "What did not go well?",
            "Share something we should start doing.",
            "Hate it? Want to stop doing something?"
        ]

        for category in self.categories:
            retro_box = RetroBox(category)
            retro_box.submit_signal.connect(self._send_text)
            self.display_boxes.update({category: retro_box})
        ##### Done with display boxes #####

        ##### Evertyhing to setting up the name ####
        self.name = LabelTextBox("Name:", orientation="H", read_only=False, line=True)
        self.set_name_button = QPushButton("Set Name")
        ##### Done with name boxes #####

        self._setup()
        self.app_man.emit("retro", {"event": "join"})

    def update(self, data: Dict):
        """
        App has been notified by Application Manager to update itself.
        Args:
            data: Data sent from the server specific for this app.
        """
        category_answers = data["category_answers"] # List of Dictionaries

        # Only fields that need to be updated int his app are display boxes. Pass data down.
        for key in category_answers:
            self.display_boxes[key].update(category_answers[key])

    def init_update(self, data):
        """
        This isnt hooked up correctly from AppManager right now.
        So this method will just pass
        """
        pass

    def _setup(self):
        """
        Prepare the View and connect things
        """
        # Set name fields
        self.set_name_button.clicked.connect(self.set_name)
        self.name_row.addWidget(self.name)
        self.name_row.addWidget(self.set_name_button)

        # Show all display boxes
        self.row_one.addWidget(self.display_boxes[self.categories[0]])
        self.row_one.addWidget(self.display_boxes[self.categories[1]])
        self.row_two.addWidget(self.display_boxes[self.categories[2]])
        self.row_two.addWidget(self.display_boxes[self.categories[3]])

        # Add Everything to the layout
        self.layout.addLayout(self.name_row)
        self.layout.addLayout(self.row_one)
        self.layout.addLayout(self.row_two)
        self.setLayout(self.layout)

    def set_name(self):
        """
        Verifies name and emits name data to server
        """
        # Make sure that set name is not being called else where.
        # Should only be able to enter method if user is elibile to set name (isEnabled)
        if self.name.isEnabled():
            # Error for no name value
            if len(self.name.text()) == 0:
                print("Enter a name!")
                return
            # Users can only set name once. Disable edit label and button
            self.name.setDisabled(True)
            self.set_name_button.setDisabled(True)

            # Create name payload and emit data
            name_payload = {
                "event": "join",
                "name": self.name.text()
            }
            self.app_man.emit("retro", name_payload)

            # Enable all entry boxes.
            for category in self.categories:
                self.display_boxes[category].setEnabled(True)

    def _send_text(self, payload):
        """
        Wrapper to emit entry data from retro boxes.
        """
        payload.update({
            "user": self.name.text()
        })
        AppManager().emit("retro", payload)
