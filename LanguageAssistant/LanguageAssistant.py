#Задача 1 (15 баллов). 

#Давайте сделаем примитивного голосового помощника, задача которого - помогать пользователю изучать выбранный язык. Такая программа должна уметь следующие вещи: 

#- разговаривать с пользователем голосом (и распознавать его речь)
#- знать команды "переведи" и "зачитай вслух". Обе команды заставляют программу предложить пользователю ввести текст, который потом переводится и/или зачитывается программой. 
#- знать команду "практика": программа предлагает пользователю небольшой текст, выбранный случайным образом из базы данных программы. Пользователь должен зачитать текст вслух, а программа должна сравнить распознанный голос пользователя с исходным текстом и сообщить, если не совпало. 
#- опционально можно добавить функцию для ручного пополнения базы данных. 

#Язык выбираете какой угодно (из поддерживаемых библиотеками, конечно). '''


import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import pygame
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QIcon

class LangAssistantWithInterface(QWidget):

    def __init__(self):
        super().__init__()
        self.lang = 'es'
        self.setWindowTitle('My simple language assistant ^-^')
        self.setGeometry(300, 300, 600, 600) # размер окна
        self.setWindowIcon(QIcon('icon.png'))

        pygame.init() # чтобы потом аудио включить

        layout = QVBoxLayout() # main layout

        # ставлю картинку на заставку
        self.setStyleSheet('background-image: url(background.png);')

        self.label = QLabel('¡Hola! Хотите перевести, почитать или потренироваться? Введите текст в этом окне и выберите команду!')
        self.label.setFont(QFont('Calibri', 12))
        layout.addWidget(self.label)

        # место для ввода текста пользователя
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        
        mid_layout = QHBoxLayout() # layout посередине
        # место для вывода перевода
        self.output = QTextEdit()
        mid_layout.addWidget(self.output)
        # место для комментариев от программы
        self.appcomments = QTextEdit()
        mid_layout.addWidget(self.appcomments)

        layout.addLayout(mid_layout)

        bottom_layout = QVBoxLayout() # layout внизу

        # кнопки с командами
        self.button1 = QPushButton('☆Перевести текст ru -> es☆')
        self.button1.clicked.connect(self.translate)
        self.button1.setFont(QFont('Calibri', 12))
        bottom_layout.addWidget(self.button1)

        self.button11 = QPushButton('☆Перевести текст es -> ru☆')
        self.button11.clicked.connect(self.translate2)
        self.button11.setFont(QFont('Calibri', 12))
        bottom_layout.addWidget(self.button11)

        self.button2 = QPushButton('☆Прочитать текст вслух☆')
        self.button2.clicked.connect(self.readaloud)
        self.button2.setFont(QFont('Calibri', 12))
        bottom_layout.addWidget(self.button2)

        self.button3 = QPushButton('☆Практика испанского☆')
        self.button3.clicked.connect(self.recognizespeech)
        self.button3.setFont(QFont('Calibri', 12))
        bottom_layout.addWidget(self.button3)

        self.button4 = QPushButton('☆Перевести и прочитать☆')
        self.button4.clicked.connect(self.translate_and_readaloud)
        self.button4.setFont(QFont('Calibri', 12))
        bottom_layout.addWidget(self.button4)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def translate(self): # перевод ru -> es +
        user_input = self.text_edit.toPlainText()
        sourcelang = 'ru'   
        translator = Translator()
        translated_text = translator.translate(user_input, src=sourcelang, dest=self.lang)
        # вывод текста
        self.output.setPlainText(translated_text.text)

    def translate2(self): # перевод es -> ru +
        user_input = self.text_edit.toPlainText()
        targetlang = 'ru'   
        translator = Translator()
        translated_text = translator.translate(user_input, src=self.lang, dest=targetlang)
        # вывод текста
        self.output.setPlainText(translated_text.text)    

    def readaloud(self, text): # озвучивает текст на испанском +
        text = self.text_edit.toPlainText()
        msg = 'читаю ваш текст...'
        tts = gTTS(text=text, lang='es')
        tts.save('output.mp3')
        pygame.mixer.music.load('output.mp3')
        pygame.mixer.music.play()
        # вывод 
        self.appcomments.setPlainText(msg) 

    def translate_and_readaloud(self): # перевести и прочитать ru -> es работает!!!
        user_input = self.text_edit.toPlainText()
        msg = 'читаю и перевожу ваш текст...'
        sourcelang = 'ru' 
        translator = Translator()
        translated_text = translator.translate(user_input, src=sourcelang, dest=self.lang)
        tts = gTTS(text = str(translated_text.text), lang=self.lang)
        tts.save('translation_output.mp3')
        pygame.mixer.music.load('translation_output.mp3')
        pygame.mixer.music.play()
        # вывод текста
        self.output.setPlainText(translated_text.text)
        # вывод 
        self.appcomments.setPlainText(msg) 

    def recognizespeech(self): # для практики произношения на испанском +
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.appcomments.setPlainText('говорите...')
            audio = recognizer.listen(source)
        # вывод ответа программы
            self.output.setPlainText('Вы произнесли: ' + recognizer.recognize_google(audio, language=self.lang))
            if self.text_edit.toPlainText() == recognizer.recognize_google(audio, language=self.lang):
                self.appcomments.setPlainText('¡Muy bien! Продолжайте в том же духе ^_^')
            else:
                self.appcomments.setPlainText('Вам стоит потренироваться ещё. Вы произнесли:' + recognizer.recognize_google(audio, language=self.lang))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LangAssistantWithInterface()
    window.show()
    sys.exit(app.exec_())