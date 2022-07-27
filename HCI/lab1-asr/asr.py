from PyQt5 import QtWidgets, QtGui, QtCore, uic

from asrInterface import Ui_MainWindow
import sys

import speech_recognition as sr
import guessTheWord
import time
import subprocess
import threading


class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def waitForInput(recog, micro):
    while True:
        print("recognizing")
        application.ui.listeningUi()
        guess = guessTheWord.recognize_speech_from_mic(recog, micro)
        if guess["transcription"]:
            print(guess["transcription"])
            if guess["transcription"] == "play music":
                playMusic()
            elif guess["transcription"] == "open file" or \
                    guess["transcription"] == "open final" or \
                    guess["transcription"] == "open trail":
                openFile()
            else:
                notCatch()
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            notCatch()

def playMusic():
    application.ui.playMusicUi()
    music_pro = subprocess.Popen(["afplay","101.mp3"])
    time.sleep(10)
    music_pro.kill()


def openFile():
    application.ui.openFileUi()
    file_pro = subprocess.Popen(["open","-e","file.txt"])

def notCatch():
    application.ui.notCatchUi()
    time.sleep(3)


app = QtWidgets.QApplication([])
application = myWindow()
recognizer = sr.Recognizer()
microphone = sr.Microphone()
application.show()
t = threading.Thread(target=waitForInput,args=(recognizer,microphone))
t.start()
sys.exit(app.exec())


