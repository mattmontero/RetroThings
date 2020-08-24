
import logging

from PySide2 import QtCore

from PySide2.QtWidgets import QLabel, QWidget, QPushButton, QInputDialog
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QScrollArea
from PySide2.QtCore import Signal
from app_manager import AppManager
from components.retro_tile import RetroTile, RetroDialog

class TileList(QWidget):
    def __init__(self, orientation="v", *args, **kwargs):
        super(TileList, self).__init__(*args, **kwargs)
        self.layout = QVBoxLayout() if orientation == "v" else QHBoxLayout()
        self._align = QtCore.Qt.AlignTop if orientation == "v" else QtCore.Qt.AlignLeft
        self.layout.setAlignment(self._align)
        self.layout.setSpacing(0)
        self._list = list()
        self.setLayout(self.layout)

    def addWidget(self, tile_data, signal):
        """
        Add widget is called every time a backend update is emitted
        This will either update the widget or create a new one
        """
        for retro_tile in self._list:
            if retro_tile.id == tile_data["response_id"]:
                retro_tile.update(tile_data)
                return
        new_tile = RetroTile(tile_data)
        new_tile.update_signal.connect(signal)
        self._list.append(new_tile)
        self.layout.addWidget(new_tile)

class RetroBox(QWidget):
    """
    This box contains a lable component and text entry field.
    """
    # submit_signal should be connected to the owning app.
    # This is emited any time that an entry is submitted
    submit_signal = Signal(dict)
    def __init__(self, label, *args, **kwargs):
        super(RetroBox, self).__init__(*args, **kwargs)
        self.setContentsMargins(QtCore.QMargins(0,0,0,0))
        self.layout = QVBoxLayout()
        #|------------------------------|
        #| [Label Text] [Add-Button]    |
        #| |--------------------------| |
        #| ||------------------------|| |
        #| ||      [Retro Tile]      || |
        #| ||------------------------|| |
        #| |                          | |
        #| |                          | |
        #| |--------------------------| |
        #|------------------------------|
        
        # Header has Label and Add Button #
        self.header = QHBoxLayout()
        self.label = QLabel(label)
        self.add_button = QPushButton("+")
        # End Header #

        # Scroll Area Components #
        # TODO: Create a component to contain both tile_list and QScrollArea
        self.tile_list = TileList()
        self.scroll_area = QScrollArea(self)

        # This is a data field. It contains all info from the server for this corresponding box
        # This is used to update the scroll area tiles
        self.retro_tiles_list = list()
        # Scroll Area CComponents #

        self._setup()

    def _setup(self):
        """ Set initial view state and connect things """
        # By Default, add acction is disabled
        self.add_button.setEnabled(False)

        # Scroll area component #
        self.scroll_area.setFixedSize(500,200)
        self.scroll_area.setWidget(self.tile_list)
        self.scroll_area.setWidgetResizable(True)

        # Header Component #
        self.add_button.clicked.connect(self.accept_input)
        self.add_button.setFixedSize(50, 50)
        self.header.addWidget(self.label)
        self.header.addWidget(self.add_button)

        # Add to layout #
        self.layout.addLayout(self.header)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

    def init_update(self, data):
        """ init_update is not hooked up correctly from Application Manager. Pass for now... """
        pass

    def update(self, data):
        """
        This update is invoked by the its parent app.
        The Parent app should pass down the server data since the parent app
        is a listener for AppMan updates
        """
        self.retro_tiles_list = data
        for tile in self.retro_tiles_list:
            self.tile_list.addWidget(tile, self.update_signal)

    def setEnabled(self, enabled):
        """
        Enable the add button
        Args:
            enabled: True or False
        """
        self.add_button.setEnabled(enabled)

    def update_signal(self, payload):
        """
        This is a signal that is triggered if there is an update event from the
        Edit/Read modal. Propegate up to parent app.
        """
        if len(payload["user_response"]) == 0:
            # No update, maybe delete?
            return

        payload.update({
            "event": "update_submission",
            "category": self.label.text()
        })
        self.submit_signal.emit(payload)

    def accept_input(self):
        """
        This Displays a Dialog that accepts input.
        This is called when user wants to add a response
        """
        text, ok = QInputDialog().getMultiLineText(self, self.label.text(),
                                          self.label.text())
        if len(text) == 0 or not ok:
            return

        payload = {
            "event": "submission",
            "category": self.label.text(),
            "user_response": text
        }
        self.submit_signal.emit(payload)
