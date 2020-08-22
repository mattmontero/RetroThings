
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
        self.add_button.setEnabled(False)
        # End Header #

        # Scroll Area #
        self.tile_list = TileList()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setFixedSize(500,200)
        self.scroll_area.setWidget(self.tile_list)
        self.scroll_area.setWidgetResizable(True)

        # Tile Panel #
        self.tile_panel = QVBoxLayout()
        self.retro_tiles_list = list()
        # End Tile Panel components #

        self._setup()

    def _setup(self):
        self.add_button.clicked.connect(self.accept_input)
        self.add_button.setFixedSize(50, 50)
        self.header.addWidget(self.label)
        self.header.addWidget(self.add_button)

        self.layout.addLayout(self.header)
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)

    def init_update(self, data):
        print("Just joined? Let's set up all the data we know about")
        pass

    def update(self, data):
        self.retro_tiles_list = data
        for tile in self.retro_tiles_list:
            self.tile_list.addWidget(tile, self.update_signal)

    def setEnabled(self, enabled):
        self.add_button.setEnabled(enabled)

    def update_signal(self, payload):
        if len(payload["user_response"]) == 0:
            # No update, maybe delete?
            return

        payload.update({
            "event": "update_submission",
            "category": self.label.text()
        })
        self.submit_signal.emit(payload)

    def accept_input(self):
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