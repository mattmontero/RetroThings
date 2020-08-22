import logging
import sys
from typing import List

import requests
import socketio
import time

from PySide2 import QtCore
from PySide2.QtCore import QThread, Signal, QObject
from store import create_store


class AppManager(QObject):
    server_state = dict()
    singleton = None

    class __SingleAppManager(QThread):
        update_signal = Signal(dict)
        def __init__(self, app_manager):
            super(type(self), self).__init__()
            sio = socketio.Client()
            self.app_manager = app_manager

            @sio.event
            def connect():
                print("Socket connection established")

            @sio.on("server_update")
            def server_update(data):
                self.update_signal.emit(data)

            @sio.event
            def disconnect():
                print('disconnected from server')

            self.sio = sio

        def run(self):
            print("Attempting to connect")
            self.sio.connect("http://localhost:3005")

        def relay(self, point, payload):
            self.sio.emit(point, payload)

    def __init__(self):
        super(AppManager, self).__init__()
        self.stores = create_store()

        if not AppManager.singleton:
            start = time.perf_counter()
            # Create Socket
            AppManager.singleton = AppManager.__SingleAppManager(self)
            # Connect Signal to update
            self.singleton.update_signal.connect(self.update)
            # Start thread
            AppManager.singleton.start()
            stop = time.perf_counter()

        self.sio = AppManager.singleton.sio
        self._emit = self.sio.emit
        self._app = self._main_widget = self._main_layout = None
        self._is_running = False

    def emit(self, event, payload):
        """ Wrap all emits to send user info """
        payload.update({"user": self.sio.sid})
        self._emit(event, payload)

    def connect_qt(self, app, main_widget, main_layout):
        self._app = app
        self._main_widget = main_widget
        self._main_layout = main_layout

    def destroy(self):
        self.sio.disconnect()
        self.emit = None
        self.sio = None
        self.stores = None
        AppManager.singleton = None

    def add_widget(self, widget, subscriber: List[str]):
        subscriber.append('init')
        # Subscribe to server updates
        for subscribe in subscriber:
            self.stores[subscribe].append(widget)

        self._main_layout.addWidget(widget)

        # Update new widget with current server state
        widget.init_update(AppManager.server_state)

    def update(self, data):
        widgets = list()
        AppManager.server_state = data['server']
        init = data['store'] if data['store'] == "init" else None
        if not init:
            widgets = self.stores[data['store']]

        for widget in widgets:
            widget.update(data)

    def run(self):
        if self._is_running:
            return
        self._is_running = True
        self._main_widget.show()
        self._app.exec_()
