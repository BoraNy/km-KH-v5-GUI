import os
from multiprocessing import Process
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from pocketsphinx import LiveSpeech
import dictionary
from random import randint

def LiveSpeechToText():
    def get_response(input_text):
        if input_text in dictionary.khmer_greeting:
            return dictionary.khmer_greeting[randint(0, 1)]
        if input_text in dictionary.khmer_farewell:
            return dictionary.khmer_farewell[randint(0, 1)]
        return '--ពុំមាននៅក្នុងសំណុំទិន្នន័យ--'

    model_dir = '/home/freak/MEGAsync/'

    # Setup Speech to Text Config
    speech_recognition = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        agc='noise',
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        kws_threshold=1e-20,
        hmm=f'{model_dir}/km-KH-v5/model_parameters/km-KH-v5.ci_cont/',
        lm=f'{model_dir}/km-KH-v5/etc/km-KH-v5.lm.DMP',
        dic=f'{model_dir}/km-KH-v5/etc/km-KH-v5.dic'
    )

    for speech in speech_recognition:
        speech = str(speech)

        # Automatic Response
        respond = get_response(speech)
        
        ### Output Audio Respond
        if respond != '--ពុំមាននៅក្នុងសំណុំទិន្នន័យ--':
        	os.system(f'play audio/{respond}.wav')

        # Print to terminal
        print(f'{speech} | {respond}')

        # Split string to array of words
        khmer_mic_input_unicode_to_khmer = ''
        robot_respond_unicode_to_khmer = ''

        unicode_str = speech.split()
        respond = str(respond).split()

        # Convert Microphone Input to Khmer
        for word in unicode_str:
            try:
                microphone_unicode_to_khmer = dictionary.UnicodeToKhmerDictionary[f'{word}']
                khmer_mic_input_unicode_to_khmer += f'{microphone_unicode_to_khmer}'
            except KeyError:
                khmer_mic_input_unicode_to_khmer += f'{word}'

        # Convert Robot Respond to Khmer
        for word in respond:
            try:
                robot_unicode_to_khmer = dictionary.UnicodeToKhmerDictionary[f'{word}']
                robot_respond_unicode_to_khmer += f'{robot_unicode_to_khmer}'
            except KeyError:
                robot_respond_unicode_to_khmer += f'{respond}'

        return khmer_mic_input_unicode_to_khmer, robot_respond_unicode_to_khmer


def UserInterface():
	class Ui_MainWindow(object):

        ### start usr define func
		def UpdateKhmerTextOnGUI(self, text_update):
			self.KhmerTextReceivedFromSTT.setText(f'{text_update[0]}')
			self.KhmerTextRespondFromRobot.setText(f'{text_update[1]}')

		def RunUpdateKhmerTextOnGUI(self):
			temp_string = LiveSpeechToText()
			self.UpdateKhmerTextOnGUI(text_update=temp_string)

		def ExitGUI(self):
			sys.exit('Program Closed')
			self.worker.disconnect()
			self.thread.terminate()

		def ResetGUIVariable(self):
			self.KhmerTextReceivedFromSTT.clear()
			self.KhmerTextRespondFromRobot.clear()

        ### end usr define fnc

		def setupUi(self, MainWindow):
		    MainWindow.setObjectName("MainWindow")
		    MainWindow.resize(480, 284)
		    font = QtGui.QFont()
		    font.setFamily("Noto Mono")
		    MainWindow.setFont(font)
		    MainWindow.setWindowTitle("Khmer Automatic Speech Recognition")
		    icon = QtGui.QIcon()
		    icon.addPixmap(QtGui.QPixmap("img/Icon_NPIC_Logo_Khmer.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		    MainWindow.setWindowIcon(icon)
		    MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
		    self.ExitPushButton = QtWidgets.QPushButton(MainWindow)
		    self.ExitPushButton.setGeometry(QtCore.QRect(372, 220, 89, 41))
		    font = QtGui.QFont()
		    font.setFamily("Khmer OS Battambang")
		    font.setPointSize(12)
		    self.ExitPushButton.setFont(font)
		    self.ExitPushButton.setObjectName("ExitPushButton")
		    self.ResetPushButton = QtWidgets.QPushButton(MainWindow)
		    self.ResetPushButton.setGeometry(QtCore.QRect(240, 220, 121, 41))
		    font = QtGui.QFont()
		    font.setFamily("Khmer OS Battambang")
		    font.setPointSize(12)
		    self.ResetPushButton.setFont(font)
		    self.ResetPushButton.setObjectName("ResetPushButton")
		    self.KhmerTextReceivedFromSTT = QtWidgets.QTextEdit(MainWindow)
		    self.KhmerTextReceivedFromSTT.setGeometry(QtCore.QRect(20, 55, 441, 41))
		    font = QtGui.QFont()
		    font.setFamily("Khmer OS Battambang")
		    font.setPointSize(11)
		    self.KhmerTextReceivedFromSTT.setFont(font)
		    self.KhmerTextReceivedFromSTT.setToolTip("")
		    self.KhmerTextReceivedFromSTT.setWhatsThis("")
		    self.KhmerTextReceivedFromSTT.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
		    self.KhmerTextReceivedFromSTT.setObjectName("KhmerTextReceivedFromSTT")
		    self.KhmerInputInfo = QtWidgets.QLabel(MainWindow)
		    self.KhmerInputInfo.setGeometry(QtCore.QRect(20, 10, 241, 41))
		    font = QtGui.QFont()
		    font.setFamily("Khmer OS Battambang")
		    font.setPointSize(12)
		    self.KhmerInputInfo.setFont(font)
		    self.KhmerInputInfo.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
		    self.KhmerInputInfo.setFrameShadow(QtWidgets.QFrame.Raised)
		    self.KhmerInputInfo.setLineWidth(2)
		    self.KhmerInputInfo.setTextFormat(QtCore.Qt.AutoText)
		    self.KhmerInputInfo.setScaledContents(True)
		    self.KhmerInputInfo.setObjectName("KhmerInputInfo")
		    self.KhmerRespondFromInputInfo = QtWidgets.QLabel(MainWindow)
		    self.KhmerRespondFromInputInfo.setGeometry(QtCore.QRect(20, 100, 221, 51))
		    font = QtGui.QFont()
		    font.setFamily("Khmer OS Battambang")
		    font.setPointSize(12)
		    self.KhmerRespondFromInputInfo.setFont(font)
		    self.KhmerRespondFromInputInfo.setObjectName("KhmerRespondFromInputInfo")
		    self.KhmerTextRespondFromRobot = QtWidgets.QTextEdit(MainWindow)
		    self.KhmerTextRespondFromRobot.setGeometry(QtCore.QRect(20, 160, 441, 41))
		    font = QtGui.QFont()
		    font.setFamily("Khmer OS Battambang")
		    font.setPointSize(11)
		    self.KhmerTextRespondFromRobot.setFont(font)
		    self.KhmerTextRespondFromRobot.setToolTip("")
		    self.KhmerTextRespondFromRobot.setWhatsThis("")
		    self.KhmerTextRespondFromRobot.setLocale(QtCore.QLocale(QtCore.QLocale.Khmer, QtCore.QLocale.Cambodia))
		    self.KhmerTextRespondFromRobot.setObjectName("KhmerTextRespondFromRobot")
		    self.BuildInfo = QtWidgets.QLabel(MainWindow)
		    self.BuildInfo.setGeometry(QtCore.QRect(10, 250, 241, 41))
		    font = QtGui.QFont()
		    font.setFamily("Khmer OS Battambang")
		    font.setPointSize(8)
		    self.BuildInfo.setFont(font)
		    self.BuildInfo.setObjectName("BuildInfo")
		    self.line = QtWidgets.QFrame(MainWindow)
		    self.line.setGeometry(QtCore.QRect(20, 30, 441, 31))
		    self.line.setFrameShape(QtWidgets.QFrame.HLine)
		    self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
		    self.line.setObjectName("line")
		    self.line_2 = QtWidgets.QFrame(MainWindow)
		    self.line_2.setGeometry(QtCore.QRect(20, 130, 441, 31))
		    self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
		    self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		    self.line_2.setObjectName("line_2")
		    
		    ### Start User Function
		    # Update Khmer Text
		    self.timer = QTimer()
		    self.timer.setInterval(500)
		    self.timer.timeout.connect(self.RunUpdateKhmerTextOnGUI)
		    #self.timer.timeout.connect(self.ExitGUI)
		    self.timer.start()
		    
		    # Exit GUI
		    self.ExitPushButton.clicked.connect(self.ExitGUI)
		    
		    #Reset GUI Variable
		    self.ResetPushButton.clicked.connect(self.ResetGUIVariable)
		    self.retranslateUi(MainWindow)
		    QtCore.QMetaObject.connectSlotsByName(MainWindow)		    
		    
		    ### End User Function
		    
		    self.retranslateUi(MainWindow)
		    QtCore.QMetaObject.connectSlotsByName(MainWindow)

		def retranslateUi(self, MainWindow):
		    _translate = QtCore.QCoreApplication.translate
		    self.ExitPushButton.setText(_translate("MainWindow", "ចាកចេញ"))
		    self.ResetPushButton.setText(_translate("MainWindow", "កំណត់ឡើងវិញ"))
		    self.KhmerInputInfo.setText(_translate("MainWindow", "សូមនិយាយជាភាសាខ្មែរ"))
		    self.KhmerRespondFromInputInfo.setText(_translate("MainWindow", "ចម្លើយឆ្លើយតបពីរ៉ូបូត"))
		    self.BuildInfo.setText(_translate("MainWindow", "រក្សាសិទ្ធិដោយ មហាវិទ្យាល័យអេឡិចត្រូនិក​ ២០២១"))


	if __name__ == "__main__":
		import sys
		app = QtWidgets.QApplication(sys.argv)
		MainWindow = QtWidgets.QWidget()
		ui = Ui_MainWindow()
		ui.setupUi(MainWindow)
		MainWindow.show()
		sys.exit(app.exec_())
    

if __name__ == '__main__':
    ## Multi-Processing
    Process1 = Process(target=UserInterface)
    Process2 = Process(target=LiveSpeechToText)

    Process1.start()
    Process2.start()
