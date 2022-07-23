from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from design_patterns import Subscriber, Publisher
from controller import Controller
import time
from os import getcwd


class QueueScreen(QDialog, Subscriber):
    def __init__(self, app_map=None, widget=None):
        super(QueueScreen, self).__init__(name='screen')
        loadUi(getcwd()+"/screens/ui/queue.ui", self)
        self.app_map = app_map
        self.widget = widget
        self.controller = Controller('controller_screen')
        self.controller.register(self)
        self.number = 0

    def update(self, req, res=None):
        if req['command'] == 'call':
            self.call(req, res)
        

    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key.Key_Escape.value:
            #self.close()
            print("stopping...")
            self.controller.stopserver()
            time.sleep(1)
            self.widget.setCurrentIndex(self.app_map['main'])

    def start(self):
        print("starting...")
        self.controller.startserver()

    def stop(self):
        print("stopping...")
        self.controller.stopserver()


    def mod(self, val):
        self.label_6.setText(val)

    def call(self, req, res=None):

        number = req['number']
        numbersound = getcwd() + f"/sound/customer{number}.wav"
        number = f'{number:02}'

        counter = req['counter']
        countersound = getcwd() + f"/sound/station{counter}.wav"
        counter = f'{counter}'

        self.label_6.setText(number)
        self.label_5.setText(counter)

        
        effect = QSoundEffect()
        effect.setSource(QUrl.fromLocalFile(numbersound))
        #effect.setLoopCount(-2)
        effect.play()

        effect.setSource(QUrl.fromLocalFile(countersound))
        effect.play()

