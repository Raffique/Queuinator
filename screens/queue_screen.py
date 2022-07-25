from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
from PyQt6.QtCore import QUrl
from design_patterns import Subscriber, Publisher
from controller import Controller
import time
from os import getcwd, system
from sys import platform
if platform == "win32":
    import winsound


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
        elif req['command'] == 'adjust':
            self.adjust(req, res)
        

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
        numbersound = f"sound/customer{number}.wav"
        #numbersound = getcwd() + f"\sound\customer{number}.wav"
        #numbersound = numbersound.replace("\","/")

        number = f'{number:02}'

        counter = req['counter']
        countersound = f"sound/station{counter}.wav"
        #countersound = getcwd() + f"\sound\station{counter}.wav"
        #countersound = countersound.replace("\","/")
        counter = f'{counter}'

        self.label_6.setText(number)
        self.label_5.setText(counter)

        if platform == "linux" or platform == "linux2":
            system("aplay " + numbersound)
            system("aplay " + countersound)
        elif platform == "darwin":
            system("afplay " + numbersound)
            system("afplay " + countersound)
        elif platform == "win32":
            #windows soud giving issues
            winsound.PlaySound(numbersound, winsound.SND_NOSTOP)
            winsound.PlaySound(countersound, winsound.SND_NOSTOP)
        
        
        """
        #effect = QSoundEffect()
        player = QMediaPlayer()
        audio_output = QAudioOutput()
        player.setAudioOutput(audio_output)
        try:
            player.setSource(QUrl.fromLocalFile(numbersound))
            audio_output.setVolume(50)
            #effect.setLoopCount(-2)
            player.play()
        except Exception as e:
            print(e)

        print(countersound)
        try:
            player.setSource(QUrl.fromLocalFile(countersound))
            player.play()
        except Exception as e:
            print(e)
        """

    def adjust(self, req, res=None):

        number = req['number']
        number = f'{number:03}'
        self.label_6.setText(number)