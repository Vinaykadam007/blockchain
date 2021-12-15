import os
import sys
from urllib.request import urlopen
import json
import hashlib
import json
from time import sleep
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QLine, Qt, QRect, QRegExp
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
import urllib

# from blockchainCertificate import runApp 
socketserver.TCPServer.allow_reuse_address = True
#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# serverStarted = False




def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

# count = 0

class Worker1(QObject):
        global serverStarted, livestatustext, count, certificatecountlabel,blockcountlabel,activenodescountlabel,activenodesanslabel
        finished = pyqtSignal()
        progress = pyqtSignal(int)
        def run(self):
            
                # while(not serverStarted):
                sleep(5)
                while(1):
                    try:
                        print("@@@@@@@@@CLIENT SIDE@@@@@@@@@")
                        url = "http://"+serveriptextbox.text()+":"+ porttextbox.text() +"/getlivestatus"
                        response = urlopen(url)
                        data_json = json.loads(response.read())
                        print(data_json)

                        url1 = "http://localhost:"+ porttextbox.text() +"/getactivenodes"
                        response1 = urlopen(url1)
                        data_json1 = json.loads(response1.read())
                        print("##################### ",data_json1)
                        # try:
                        #         url2 = "http://localhost:"+ porttextbox.text() +"/gettransferfile"
                        #         response2 = urlopen(url2)
                        #         print("##################### ",response2)
                        # except Exception as e:
                        #         print("transfer file error: ", e)
                        # count = count + 1
                        # if count == 1:
                        #         livestatustext.appendPlainText("Certificate blockchain is running...")
                        activenodescountlabel.setText('Number of Active nodes: '+ str(data_json1['Number of active nodes']))
                        print("****************************************",str(data_json1["Active nodes are"]))
                        jsonlist = ''.join([str(elem) for elem in list(data_json1['Active nodes are'])[:-2][2:]])
                        activenodesanslabel.setText('Active nodes are: '+jsonlist)


                        certificatecountlabel.setText('Certificate count: '+str(dict(data_json)['Certificate count']))
                        blockcountlabel.setText('Number of blocks mined: '+str(dict(data_json)['Number of blocks mined']))
                        print("inside try")
                        # url = "http://localhost:"+ porttextbox.text() +"/nodes/register"
                        # response = urlopen(url)
                        # data_json = json.loads(response.read())
                        # print(data_json)
                        # count = count + 1
                        # if count == 1:
                        #         livestatustext.appendPlainText("Certificate blockchain is running...")

                        # livestatustext.appendPlainText('IP address: '+ serveriptextbox)
                        # livestatustext.appendPlainText('Port Number: '+ porttextbox)
                        # livestatustext.appendPlainText(str(data_json['Number of blocks mined']))
                        # livestatustext.setPlainText()
                        #os.system("python3 blockchaincertificate.py -p 4000 -cl 10 -noc 3")
                        sleep(2)
                    except:
                        sleep(2)
all_processes = []
thread1 = QThread()
worker1 = Worker1()
worker1.moveToThread(thread1)
thread1.started.connect(worker1.run)
worker1.finished.connect(thread1.quit)
worker1.finished.connect(worker1.deleteLater)
thread1.finished.connect(thread1.deleteLater)

class Worker(QObject):
        global thread1,serveriptextbox,maxnoofblockstextbox, porttextbox,youriptextbox, browsetextbox
        finished = pyqtSignal()
        progress = pyqtSignal(int)
        def run(self):
                print("")
                thread1.start()
                # tempapp = runApp()
                # tempapp.startApp()
                # print(serveriptextbox.text())
                all_processes.append(subprocess.Popen(['py',resource_path('post_req.py'),'-ip',serveriptextbox.text(),'-yourip',youriptextbox.text(),'-p', porttextbox.text()], stdout=subprocess.PIPE))
                # stdout = process.communicate()[0]
                print('******************************************************************************************************************')
                
        #         os.system("py post_req.py -ip {0} -p {1}".format(serveriptextbox.text(),porttextbox.text()))
        #         serverStarted = True
        # #self.finished.emit()




thread = QThread()
worker = Worker()
worker.moveToThread(thread)
thread.started.connect(worker.run)
worker.finished.connect(thread.quit)
worker.finished.connect(worker.deleteLater)
thread.finished.connect(thread.deleteLater)





class MainWindow(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI()
                self.setFixedSize(700, 320)
        def initUI(self):
                global name, addtransactiondialog, filedata, browsetextbox, youriptextbox,connectinglabel,livestatustext,serveriptextbox, porttextbox, count, thread, thread1,certificatecountlabel,blockcountlabel,activenodescountlabel,activenodesanslabel
                
                #self.worker.progress.connect(self.reportProgress)
                #self.thread.start()

                self.setWindowFlags( Qt.WindowCloseButtonHint |  Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
                self.setWindowTitle('Client Section')
                icon_path = resource_path('python.ico')
                self.setWindowIcon(QIcon(str(icon_path)))
                Glayout = QGridLayout()
                
                hlayout = QHBoxLayout()
                honelayout = QHBoxLayout()
                htwolayout = QHBoxLayout()
                hthreelayout = QHBoxLayout()
                hfourlayout = QHBoxLayout()

                vlayout = QVBoxLayout()
                vonelayout = QVBoxLayout()
                vtwolayout = QVBoxLayout()
                #self.obj = blockchaincertificate.Worker()
                #self.thread = QThread()
                #self.obj.moveToThread(self.thread)
                #self.obj.finished.connect(self.thread.quit)
                #self.thread.started.connect(self.obj.run)
                #self.thread.start()


                #self.experimentlabel = QLabel("Blockchain Experiment Selection",self)
                #self.experimentlabel.setFixedWidth(200)

                #self.livestatuslabel = QLabel("Live status",self)
                #self.livestatuslabel.setFixedWidth(100)
                vframe = QFrame(self)
                vframe.setGeometry(QRect(320, 150, 118, 3))
                vframe.setFrameShape(vframe.VLine)
                vframe.setFrameShadow(vframe.Sunken)

                hframe = QFrame(self)
                hframe.setGeometry(QRect(320, 150, 118, 3))
                hframe.setFrameShape(hframe.HLine)
                hframe.setFrameShadow(hframe.Sunken)

                hframe1 = QFrame(self)
                hframe1.setGeometry(QRect(320, 150, 118, 3))
                hframe1.setFrameShape(hframe1.HLine)
                hframe1.setFrameShadow(hframe1.Sunken)

                hframe2 = QFrame(self)
                hframe2.setGeometry(QRect(320, 150, 118, 3))
                hframe2.setFrameShape(hframe2.HLine)
                hframe2.setFrameShadow(hframe2.Sunken)


                startbutton = QPushButton("Connect", self)
                startbutton.clicked.connect(self.on_start)
                startbutton.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                startbutton.setFixedHeight(35)

                stopbutton = QPushButton("Disconnect", self)
                stopbutton.clicked.connect(self.on_stop)
                stopbutton.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                stopbutton.setFixedHeight(35)

                #self.startbutton.setStyleSheet('QPushButton {  border-color: white; border-width: 1px; padding: 14px; border-style: outset; border-radius: 6px; background-color: #1c9c1e; font-weight:regular;fo>                self.startbutton.setCursor(QCursor(Qt.PointingHandCursor))

                
                addtransactionbutton = QPushButton("Add Certificate", self)
                addtransactionbutton.clicked.connect(self.add_transaction)
                #self.blockchainviewbutton.setStyleSheet('QPushButton {  border-color: white; border-width: 1px; padding: 14px; border>
                addtransactionbutton.setCursor(QCursor(Qt.PointingHandCursor))
                addtransactionbutton.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                addtransactionbutton.setFixedHeight(35)


                blockchainviewbutton = QPushButton("View Blockchain", self)
                blockchainviewbutton.clicked.connect(self.view_blockchain)
                blockchainviewbutton.setCursor(QCursor(Qt.PointingHandCursor))
                blockchainviewbutton.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                blockchainviewbutton.setFixedHeight(35)

                # walletviewbutton = QPushButton("View Wallet", self)
                # walletviewbutton.clicked.connect(self.on_click)
                # #self.walletviewbutton.setStyleSheet('QPushButton {  border-color: white; border-width: 1px; padding: 14px; border>
                # walletviewbutton.setCursor(QCursor(Qt.PointingHandCursor))
                # walletviewbutton.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                # walletviewbutton.setFixedHeight(35)




                # self.cb = QComboBox()
                # self.cb.addItem("Certificate")
                # self.cb.addItem("Cryptocurrency")
                # self.cb.currentIndexChanged.connect(self.selectionchange)
                # self.cb.setStyleSheet("font-weight: bold; font-size: 10pt; font-family: Seoge UI; color: black;")
                
                livestatuslabel = QLabel("Live status",self)
                livestatuslabel.setFixedWidth(200)
                livestatuslabel.setStyleSheet("font-weight: bold; font-size: 10pt; font-family: Seoge UI; color: black;")

                activenodeslabel = QLabel("Active Nodes",self)
                activenodeslabel.setFixedWidth(200)
                activenodeslabel.setStyleSheet("font-weight: bold; font-size: 10pt; font-family: Seoge UI; color: black;")

                configuretextlabel = QLabel("Blockchain Configurations",self)
                configuretextlabel.setFixedWidth(200)
                configuretextlabel.setStyleSheet("font-weight: bold; font-size: 10pt; font-family: Seoge UI; color: black;")

                serveriplabel = QLabel("Server IP Address",self)
                serveriplabel.setFixedWidth(200)
                serveriplabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")


                # maxnoofblockslabel = QLabel("Max no of blocks",self)
                # maxnoofblockslabel.setFixedWidth(200)
                youriplabel = QLabel("Your IP Address",self)
                youriplabel.setFixedWidth(200)
                youriplabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                portlabel = QLabel("Port number",self)
                portlabel.setFixedWidth(200)
                portlabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                certificatecountlabel = QLabel("",self)
                certificatecountlabel.setFixedWidth(200)
                certificatecountlabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                blockcountlabel = QLabel("",self)
                blockcountlabel.setFixedWidth(200)
                blockcountlabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                connectinglabel = QLabel("",self)
                connectinglabel.setFixedWidth(200)
                connectinglabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")



                activenodescountlabel = QLabel("",self)
                activenodescountlabel.setFixedWidth(200)
                activenodescountlabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                activenodesanslabel = QLabel("",self)
                activenodesanslabel.setFixedWidth(300)
                activenodesanslabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                #self.cb.setFixedHeight(150)
                # configuretext = QPlainTextEdit(self)
                # configuretext.setReadOnly(True)
                # configuretext.insertPlainText("Blockchain Configurations")
                #self.configuretext.setStyleSheet("QPlainTextEdit { background-color: black; color: green; font-size: 10pt;}")
                
                serveriptextbox = QLineEdit(self)
                # serveriptextbox.move(20, 20)
                serveriptextbox.resize(20,20)
                serveriptextbox.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                # maxnoofblockstextbox = QLineEdit(self)
                # serveriptextbox.move(20, 20)
                # maxnoofblockstextbox.resize(20,20)

                porttextbox = QLineEdit(self)
                # serveriptextbox.move(20, 20)
                porttextbox.resize(20,20)
                porttextbox.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                youriptextbox = QLineEdit(self)
                # serveriptextbox.move(20, 20)
                youriptextbox.resize(20,20)
                youriptextbox.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                # livestatustext = QPlainTextEdit(self)
                # livestatustext.setReadOnly(True)
                # livestatustext.insertPlainText("")


                # activenodestext = QPlainTextEdit(self)
                # activenodestext.setReadOnly(True)
                # activenodestext.insertPlainText("")



                



                #Glayout.addWidget(self.experimentlabel,0,0)
                # Glayout.addWidget(cb,0,0)
                Glayout.addLayout(vtwolayout,0,0)
                # vtwolayout.addWidget(self.cb)
                vtwolayout.addWidget(hframe1)
                vtwolayout.addWidget(livestatuslabel)
                # Glayout.addWidget(livestatustext,1,0)
                vtwolayout.addWidget(connectinglabel)
                vtwolayout.addWidget(certificatecountlabel)
                vtwolayout.addWidget(blockcountlabel)
                #Glayout.addWidget(self.livestatuslabel,2,0)
                Glayout.addWidget(vframe,0,1)
                Glayout.addLayout(vonelayout,0,2)
                vonelayout.addWidget(configuretextlabel)


                vonelayout.addLayout(vlayout)
                vlayout.addLayout(honelayout)
                
                honelayout.addWidget(youriplabel)
                honelayout.addWidget(youriptextbox)

                

                vlayout.addLayout(htwolayout)
                htwolayout.addWidget(serveriplabel)
                htwolayout.addWidget(serveriptextbox)

                vlayout.addLayout(hthreelayout)
                hthreelayout.addWidget(portlabel)
                hthreelayout.addWidget(porttextbox)

                vlayout.addLayout(hfourlayout)
                hfourlayout.addWidget(startbutton)
                hfourlayout.addWidget(stopbutton)
                
                vlayout.addWidget(QWidget())
                vlayout.addWidget(QWidget())
                vlayout.addWidget(hframe)
                vlayout.addWidget(activenodeslabel)
                vlayout.addWidget(activenodescountlabel)
                vlayout.addWidget(activenodesanslabel)
                vlayout.addWidget(hframe2)
                vlayout.addLayout(hlayout)
                
                hlayout.addWidget(addtransactionbutton)
                hlayout.addWidget(blockchainviewbutton)
                # hlayout.addWidget(walletviewbutton)
                # Glayout.addLayout(hlayout,3,2)

                #vlayout.addWidget(self.experimentlabel)
                #hlayout.addWidget(self.cb)
                self.setLayout(Glayout)


        # def selectionchange(self,i):
        #         for count in range(self.cb.count()):
        #                 print(self.cb.itemText(count))
        #         print("Current index", i, "selection changed", self.cb.currentText())
        def on_click(self):
                print("clicked")
        def add_transaction(self):
                global browsetextbox, addtransactiondialog
                print("Add Certificate")
                self.w = addcertificate()
                self.w.show()
                # self.hide()
                # all_processes.append(subprocess.Popen(['py',resource_path('post_req_transaction.py'),'-ip',serveriptextbox.text(),'-filename','temp.pdf' ,'-filedata','nskjsfnvjsnfvkjsnv'], stdout=subprocess.PIPE))
                
                # addtransactiondialog = QDialog()
                # addtransactiondialog.setModal(True)
                # addtransactiondialog.setWindowTitle("Send Certificate")
                # addtransactiondialog.setFixedSize(700, 100)
                # icon_path = resource_path('python.ico') #os.path.realpath("enablAR.ico") #Path(__file__).parent / "../icons/enablAR.ico"
                # addtransactiondialog.setWindowIcon(QIcon(str(icon_path)))

                
                
               

                # addtransactiondialog.exec_()

       
        def view_blockchain(self):
                print("view blockchain windows")
                try:
                        url = "http://localhost:"+ porttextbox.text() +"/chain"
                        response = urlopen(url)
                        data_json = json.loads(response.read())
                        print(data_json['chain'])
                        viewblockchaindialog = QDialog()
                        viewblockchaindialog.setModal(True)
                        viewblockchaindialog.setWindowTitle("Blockchain section")
                        viewblockchaindialog.setFixedSize(700, 300)
                        icon_path = resource_path('enablAR.ico') #os.path.realpath("enablAR.ico") #Path(__file__).parent / "../icons/enablAR.ico"
                        viewblockchaindialog.setWindowIcon(QIcon(str(icon_path)))



                        



                        msglabel = QPlainTextEdit(viewblockchaindialog)
                        msglabel.setReadOnly(True)
                        msglabel.setFont(QFont('Seoge UI', 10))
                        msglabel.setFixedSize(700, 300)
                        msglabel.setPlainText("")
                        # print(str(data_json['chain']))
                        # print("LLLLLLLLLLLLLLLLLLLLLLLLL")
                        # print(list(data_json['chain'][0]))
                        for i in range(int(data_json['length'])):
                                msglabel.appendPlainText('Block '+str(i+1)+": "+str(data_json['chain'][i])+"\n")



                        viewblockchaindialog.exec_()
                except Exception as e:
                        print(e)
        def on_start(self):
                print("")
                connectinglabel.setText("Connected to \nIP "+ serveriptextbox.text() +"\nand port "+porttextbox.text()+"...")
                
                # livestatustext.setPlainText("Live status")
                # livestatustext.setPlainText("Connected")
                # # count = 0
                thread.start()
                #os.system("python3 blockchaincertificate.py -p 4000 -cl 10 -noc 3")
                #sleep(1000)
                #url = "http://172.26.156.150:5000/chain"
                #response = urlopen(url)
                #data_json = json.loads(response.read())
                 #print(data_json)
                #self.livestatustext.appendPlainText(str(data_json))
        def on_stop(self):
                print("")
                # worker.terminate()
                # thread.terminate()
                # thread1.terminate()
                # thread.wait()
                for p in all_processes:
                        p.kill()
                        print ('kill')
        def closeEvent(self,event):
                global process
                print("closing application")
                for p in all_processes:
                        p.kill()
                        print ('cleaned up!')
              

class addcertificate(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI()
                # self.setFixedSize(700, 320)
        def initUI(self):
                global browsetextbox1, name, serveriptextbox, filename
                self.setWindowTitle("Send Certificate")
                icon_path = resource_path('python.ico')
                self.setWindowIcon(QIcon(str(icon_path)))
                # self.setFixedSize(700, 100)
                # Glayout = QGridLayout()
                hbox = QHBoxLayout()
                vbox = QVBoxLayout()
                
                browsetextbox1 = QPlainTextEdit(self)
                browsetextbox1.setReadOnly(True)
                browsetextbox1.setFont(QFont('Seoge UI', 10))
                browsetextbox1.setFixedHeight(35)


                browsebutton1 = QPushButton("Browse", self)
                browsebutton1.clicked.connect(self.view_transaction)
                browsebutton1.setCursor(QCursor(Qt.PointingHandCursor))
                browsebutton1.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                browsebutton1.setFixedHeight(35)

                addcertibutton1 = QPushButton("Send certificate", self)
                addcertibutton1.clicked.connect(self.add_certi)
                addcertibutton1.setCursor(QCursor(Qt.PointingHandCursor))
                addcertibutton1.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                addcertibutton1.setFixedHeight(35)

                # Glayout.addLayout(vbox,0,0)
                vbox.addLayout(hbox)
                hbox.addWidget(browsetextbox1)
                hbox.addWidget(browsebutton1)
                hbox.addWidget(addcertibutton1)
                self.setLayout(vbox)

        def view_transaction(self):
                global browsetextbox1, filedata, name,serveriptextbox, filename
                try:
                        filter = "Certificate Files (*.PNG *.JPG *.PDF)";
                        name = QFileDialog.getOpenFileName(self, 'Browse Project', '', filter)
                        print(name[0])
                        filename = name[0].split('/')[-1]
                        print(str(name[0]).split('/')[-1])
                        browsetextbox1.setPlainText(str(name[0]))

 
                except FileNotFoundError:
                        print("file error")


        def add_certi(self):
                global filedata, name, serveriptextbox, filename
                # try:
                print("$$$$$$$$$$$$$$$$$$FILE DATA$$$$$$$$$$$$$$$$$$")
                # print(filedata) #str(name[0]).split('/')[-1]
                print('DETAILS@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                print(serveriptextbox.text())
                print("\""+filename+"\"")
                all_processes.append(subprocess.Popen(['py',resource_path('post_req_transaction.py'),'-ip',serveriptextbox.text(),'-filename',str(filename)], stdout=subprocess.PIPE))
                # os.system("py post_req_transaction.py -ip {0} -filename {1}".format(serveriptextbox.text(),str(filename)))
                print("processed")
        # except:
        #         print("add files")








def main():
        app=QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()