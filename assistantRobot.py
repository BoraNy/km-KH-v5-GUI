import threading
from os import system
from multiprocessing import Process
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from pocketsphinx import LiveSpeech
import dictionary
import sys
from random import randint
from datetime import datetime


def LiveSpeechToText():
    def get_response(input_text):
        if input_text in dictionary.khmer_greeting_polite:
            return dictionary.khmer_greeting_polite[0]

        if input_text in dictionary.khmer_greeting_general:
            return dictionary.khmer_greeting_general[0]

        if input_text in dictionary.khmer_farewell:
            return dictionary.khmer_farewell[randint(0, 1)]

        if input_text in dictionary.khmer_greeting:
            return dictionary.khmer_greeting[1]

        if input_text in dictionary.khmer_robot_name:
            return dictionary.khmer_robot_name[1]

        if input_text in dictionary.about_cambodia:
            return dictionary.about_cambodia[1]

        if input_text in dictionary.ask_time:
            temp_time = datetime.now()
            temp_time = temp_time.strftime("%H:%M")
            return temp_time
        return '--ពុំមាននៅក្នុងសំណុំទិន្នន័យ--'

    ### Khmer Speech Recognition Model
    model_dir = '/home/pi/'

    ### Setup Speech to Text Config
    speech_recognition = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=f'{model_dir}/km-KH-v5.1/model_parameters/km-KH-v5.1.ci_ptm/',
        lm=f'{model_dir}/km-KH-v5.1/etc/km-KH-v5.1.lm.DMP',
        dic=f'{model_dir}/km-KH-v5.1/etc/km-KH-v5.1.dic'
    )

    for speech in speech_recognition:
        speech = str(speech)

        ### Automatic Response
        respond = get_response(speech)

        ### Output Audio Respond
        if respond != "--ពុំមាននៅក្នុងសំណុំទិន្នន័យ--":
            system(f'aplay ./audio/{respond}.wav')

        ### Print to terminal
        print(f'{speech} | {respond}')

        # Split string to array of words
        khmer_mic_input_unicode_to_khmer = ''
        robot_respond_unicode_to_khmer = ''

        unicode_str = speech.split()
        respond = str(respond).split()

        ### Convert Microphone Input to Khmer
        for word in unicode_str:
            try:
                microphone_unicode_to_khmer = dictionary.UnicodeToKhmerDictionary[f'{word}']
                khmer_mic_input_unicode_to_khmer += f'{microphone_unicode_to_khmer}'
            except KeyError:
                khmer_mic_input_unicode_to_khmer += f'{word}'

        ### Convert Robot Respond to Khmer
        for word in respond:
            try:
                robot_unicode_to_khmer = dictionary.UnicodeToKhmerDictionary[f'{word}']
                robot_respond_unicode_to_khmer += f'{robot_unicode_to_khmer}'
            except KeyError:
                robot_respond_unicode_to_khmer += f'{respond}'

        return khmer_mic_input_unicode_to_khmer, robot_respond_unicode_to_khmer
    print("Stop live speech")


def UserInterface():
    class Ui_MainWindow(object):
        ### start usr define func
        def UpdateKhmerTextOnGUI(self, text_update):
            responseText = text_update[1].replace('[\'', '')
            responseText = responseText.replace('\']', '')
            self.KhmerTextReceivedFromSTT.setText(f'{text_update[0]}')
            self.KhmerTextRespondFromRobot.setText(f'{responseText}')

        def RunUpdateKhmerTextOnGUI(self):
            temp_string = LiveSpeechToText()
            self.UpdateKhmerTextOnGUI(text_update=temp_string)

        def ExitGUI(self):
            sys.exit('Program Closed')

        def ResetGUIVariable(self):
            self.KhmerTextReceivedFromSTT.clear()
            self.KhmerTextRespondFromRobot.clear()

        ### end usr define fnc

        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(480, 298)
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            MainWindow.setFont(font)
            MainWindow.setWindowTitle("រ៉ូបូតជំនួយការ (Assistant Robot)")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("img/Icon_NPIC_Logo_Khmer.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            MainWindow.setWindowIcon(icon)
            MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
            self.ExitPushButton = QtWidgets.QPushButton(MainWindow)
            self.ExitPushButton.setGeometry(QtCore.QRect(372, 240, 89, 41))
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            font.setPointSize(12)
            self.ExitPushButton.setFont(font)
            self.ExitPushButton.setObjectName("ExitPushButton")
            self.ResetPushButton = QtWidgets.QPushButton(MainWindow)
            self.ResetPushButton.setGeometry(QtCore.QRect(250, 240, 121, 41))
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            font.setPointSize(12)
            self.ResetPushButton.setFont(font)
            self.ResetPushButton.setObjectName("ResetPushButton")
            self.KhmerTextReceivedFromSTT = QtWidgets.QTextEdit(MainWindow)
            self.KhmerTextReceivedFromSTT.setGeometry(QtCore.QRect(20, 65, 441, 51))
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            font.setPointSize(11)
            self.KhmerTextReceivedFromSTT.setFont(font)
            self.KhmerTextReceivedFromSTT.setToolTip("")
            self.KhmerTextReceivedFromSTT.setWhatsThis("")
            self.KhmerTextReceivedFromSTT.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
            self.KhmerTextReceivedFromSTT.setObjectName("KhmerTextReceivedFromSTT")
            self.KhmerInputInfo = QtWidgets.QLabel(MainWindow)
            self.KhmerInputInfo.setGeometry(QtCore.QRect(20, 20, 381, 31))
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            font.setPointSize(13)
            self.KhmerInputInfo.setFont(font)
            self.KhmerInputInfo.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
            self.KhmerInputInfo.setFrameShadow(QtWidgets.QFrame.Raised)
            self.KhmerInputInfo.setLineWidth(2)
            self.KhmerInputInfo.setTextFormat(QtCore.Qt.AutoText)
            self.KhmerInputInfo.setScaledContents(True)
            self.KhmerInputInfo.setObjectName("KhmerInputInfo")
            self.KhmerRespondFromInputInfo = QtWidgets.QLabel(MainWindow)
            self.KhmerRespondFromInputInfo.setGeometry(QtCore.QRect(20, 120, 341, 51))
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            font.setPointSize(13)
            self.KhmerRespondFromInputInfo.setFont(font)
            self.KhmerRespondFromInputInfo.setObjectName("KhmerRespondFromInputInfo")
            self.KhmerTextRespondFromRobot = QtWidgets.QTextEdit(MainWindow)
            self.KhmerTextRespondFromRobot.setGeometry(QtCore.QRect(20, 180, 441, 51))
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            font.setPointSize(11)
            self.KhmerTextRespondFromRobot.setFont(font)
            self.KhmerTextRespondFromRobot.setToolTip("")
            self.KhmerTextRespondFromRobot.setWhatsThis("")
            self.KhmerTextRespondFromRobot.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
            self.KhmerTextRespondFromRobot.setObjectName("KhmerTextRespondFromRobot")
            self.BuildInfo = QtWidgets.QLabel(MainWindow)
            self.BuildInfo.setGeometry(QtCore.QRect(20, 250, 231, 41))
            font = QtGui.QFont()
            font.setFamily("Khmer OS Battambang")
            font.setPointSize(8)
            self.BuildInfo.setFont(font)
            self.BuildInfo.setObjectName("BuildInfo")
            self.line = QtWidgets.QFrame(MainWindow)
            self.line.setGeometry(QtCore.QRect(20, 40, 441, 31))
            self.line.setFrameShape(QtWidgets.QFrame.HLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line")
            self.line_2 = QtWidgets.QFrame(MainWindow)
            self.line_2.setGeometry(QtCore.QRect(20, 150, 441, 31))
            self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2")
            self.label = QtWidgets.QLabel(MainWindow)
            self.label.setGeometry(QtCore.QRect(420, 20, 31, 31))
            self.label.setText("")
            self.label.setPixmap(QtGui.QPixmap("img/microphone.png"))
            self.label.setScaledContents(True)
            self.label.setObjectName("label")
            self.label_2 = QtWidgets.QLabel(MainWindow)
            self.label_2.setGeometry(QtCore.QRect(420, 130, 31, 31))
            self.label_2.setText("")
            self.label_2.setPixmap(QtGui.QPixmap("img/question.png"))
            self.label_2.setScaledContents(True)
            self.label_2.setObjectName("label_2")

            ### start usr func usage
            # Update Khmer text
            self.timer = QTimer()
            self.timer.setInterval(500)
            self.timer.timeout.connect(self.RunUpdateKhmerTextOnGUI)
            self.timer.start()

            ### Exit GUI
            self.ExitPushButton.clicked.connect(self.ExitGUI)
            ### Reset GUI Variable
            self.ResetPushButton.clicked.connect(self.ResetGUIVariable)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
            ### end usr func usage

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            self.ExitPushButton.setText(_translate("MainWindow", "ចាកចេញ"))
            self.ResetPushButton.setText(_translate("MainWindow", "កំណត់ឡើងវិញ"))
            self.KhmerInputInfo.setText(_translate("MainWindow", "សូមនិយាយជាភាសាខ្មែរ (Please Speak in Khmer)"))
            self.KhmerRespondFromInputInfo.setText(
                _translate("MainWindow", "ចម្លើយឆ្លើយតបពីរ៉ូបូត (Answer from Robot)"))
            self.BuildInfo.setText(_translate("MainWindow", "រក្សាសិទ្ធិដោយ មហាវិទ្យាល័យអេឡិចត្រូនិក ២០២១"))

    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QWidget()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    ### Multi-Processing
    Process(target=UserInterface).start()
    Process(target=LiveSpeechToText).start()
