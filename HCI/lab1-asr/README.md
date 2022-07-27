# Lab 1: Automatic Speech Recognition

1753837

陈柄畅

## 1. Intro

The program can receives two kinds of user's voice command ( `Play Music` and `Open File`) , recognize the content and finish the task.

## 2. Run

```
python asr.py
```

## 3. Code

### Play Music

```python
def playMusic():
    application.ui.playMusicUi()
    music_pro = subprocess.Popen(["afplay","101.mp3"])
    time.sleep(10)
    music_pro.kill()
```

### Open File

```python
def openFile():
    application.ui.openFileUi()
    file_pro = subprocess.Popen(["open","-e","file.txt"])
```

### Recognition

```python
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
```

### Not Catch

```python
def notCatch():
    application.ui.notCatchUi()
    time.sleep(3)
```

### UI

```python
    def listeningUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow","I am listening!"))

    def playMusicUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow","Playing Music Now!"))

    def openFileUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow","Opening File Now!"))

    def notCatchUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow","I didn't catch that."))
```

### Multi-threading

```python
app = QtWidgets.QApplication([])
application = myWindow()
recognizer = sr.Recognizer()
microphone = sr.Microphone()
application.show()
t = threading.Thread(target=waitForInput,args=(recognizer,microphone))
t.start()
sys.exit(app.exec())
```

## 4. Result

[demo video](speech_recognization.mp4)

## 5. Improvement

The accuracy of `speechrecognition` is very low.

By reading README on its gitHub page, I think there are two ways to improve its performance.

First, the parameters of the recognizer can be modified such as `recognizer_instance.energy_threshold`.

Second, since the model works offline isn't large, this program can use other speech recognition api or libraries which using more powerful recognition models.