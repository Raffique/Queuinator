from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl


class MainScreen(QDialog):
    def __init__(self, app_map, widget=None):
        super(MainScreen, self).__init__()
        from os import getcwd
        loadUi(getcwd()+"/screens/ui/main.ui", self)
        self.app_map = app_map
        self.widget = widget
        self.pushButton.clicked.connect(self.start)

    def start(self):
        self.widget.setCurrentIndex(self.app_map['queue'])
        queue = self.widget.currentWidget()
        queue.start()