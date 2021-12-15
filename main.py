import os
import signal
import sys
from urllib.request import urlopen
import json
import hashlib
import json
from time import sleep
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, app, jsonify, request
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import Qt, QRect, QRegExp
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit
from PyQt5.QtGui import (QColor, QPainter, QFont, QSyntaxHighlighter,QTextFormat, QTextCharFormat)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QSplashScreen
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget
#import blockchaincertificate
from threading import Thread
from time import sleep
import socketserver
from socket import *
import socket
from argparse import ArgumentParser
import subprocess
from PyQt5.QtWidgets import QApplication, QStyle
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem


all_processes = []

def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.setFixedSize(700, 320)
    def initUI(self):
    # app = QApplication(sys.argv)
        # widget = QWidget()

        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Main Window")
        icon_path = resource_path('python.ico')
        self.setWindowIcon(QIcon(str(icon_path)))



        Hboxlayout = QHBoxLayout()
        button1 = QPushButton(self)
        button1.setText("Certificate")
        button1.move(64,32)
        button1.clicked.connect(self.button1_clicked)
        button1.setFixedWidth(200)


        button2 = QPushButton(self)
        button2.setText("Cryptocurrency")
        button2.move(64,64)
        button2.clicked.connect(self.button2_clicked)
        button2.setFixedWidth(200)

 


        Hboxlayout.addWidget(button1)
        Hboxlayout.addWidget(button2)

        self.setLayout(Hboxlayout)
        # widget.show()
        # sys.exit(app.exec_())


    def button1_clicked(self):
        print("certificate")
        all_processes.append(subprocess.Popen(['py',resource_path('blockchain_server_ui.py')], stdout=subprocess.PIPE))
        self.close()

    def button2_clicked(self):
        print("Button 2 clicked")   
    
if __name__ == '__main__':
    app=QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())