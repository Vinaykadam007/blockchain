from logging import exception
import os
import signal
import sys
from typing_extensions import runtime
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


# from blockchainCertificate import runApp 
socketserver.TCPServer.allow_reuse_address = True
#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverStarted = False
from PyQt5.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt
from PyQt5.QtWidgets import QApplication, QTreeView

# import simpletreemodel_rc


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)



def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
print(resource_path(''))
# count = 0

class Worker1(QThread):
        global serverStarted, livestatustext, count,activenodestext,certificatecountlabel,blockcountlabel,activenodescountlabel,activenodesanslabel
        textboxmsg = pyqtSignal(str)
        # def __init__(self, myString, parent =None):
        #     super().__init__()
        #     self.myString = "Certificate blockchain is running..."
        def run(self):
                sleep(1)
                print("App reaedy")
                while(1):
                    try:
                        print("@@@@@@@@SERVER SIDE@@@@@@@@@@")
                        url = "http://localhost:"+ porttextbox.text() +"/getlivestatus"
                        response = urlopen(url)
                        data_json = json.loads(response.read())
                        # print(data_json)

                        url1 = "http://localhost:"+ porttextbox.text() +"/getactivenodes"
                        response1 = urlopen(url1)
                        data_json1 = json.loads(response1.read())

                        # try:
                        #         url2 = "http://localhost:"+ porttextbox.text() +"/gettransferfile"
                        #         response2 = urlopen(url2)
                        #         print("##################### ",response2)
                        # except Exception as e:
                        #         print("transfer file error: ", e)


                        try:
                                # self.textboxmsg.emit(self.myString)
                                # activenodestext.setPlainText('Number of Active nodes: {0}'.format(data_json1['Number of active nodes']))
                                # activenodestext.clear()
                                # activenodestext.setPlainText("hello")
                                # activenodestext.setPlainText('Active nodes are: '+str(dict(data_json1)['Active nodes are']))
                                # app.livestatustext.setPlainText("hello")
                                # livestatustext.setPlainText("Certificate blockchain is running...")
                                # livestatustext.appendPlainText('Certificate count: '+str(dict(data_json)['Certificate count']))
                                # livestatustext.appendPlainText('Number of blocks mined: '+str(dict(data_json)['Number of blocks mined']))
                                activenodescountlabel.setText('Number of Active nodes: '+ str(data_json1['Number of active nodes']))
                                print(len(list(data_json1['Active nodes are'])))
                                if len(list(data_json1['Active nodes are']))<= 5:
                                        activenodesanslabel.setText('Active nodes are: ')
                                else:
                                        jsonlist = ''.join([str(elem) for elem in list(data_json1['Active nodes are'])[:-2][2:]])
                                        activenodesanslabel.setText('Active nodes are: '+jsonlist)


                                certificatecountlabel.setText('Certificate count: '+str(dict(data_json)['Certificate count']))
                                blockcountlabel.setText('Number of blocks mined: '+str(dict(data_json)['Number of blocks mined']))
                                print("inside try")
                                # livestatustext.moveCursor(QTextCursor.End)
                                # activenodestext.moveCursor(QTextCursor.End)
                        except Exception as e:
                                print("error: ",e)
                                sleep(2)
                        # sleep(3)
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
        global thread1,noofcertificatestextbox,maxnoofblockstextbox, porttextbox, process
        finished = pyqtSignal()
        progress = pyqtSignal(int)
        def run(self):
                print("")
                thread1.start()
                # tempapp = runApp()
                # tempapp.startApp()
                # print(noofcertificatestextbox.text())
                print(resource_path(''))
                all_processes.append(subprocess.Popen(['py',resource_path('blockchainCertificate.py') ,'-p',porttextbox.text() ,'-cl', maxnoofblockstextbox.text() ,'-noc', noofcertificatestextbox.text()], stdout=subprocess.PIPE ,shell=True))


              
                # stdout = process.communicate()[0]
                print('******************************************************************************************************************')
                # print(stdout, process.returncode)
                # os.system("py blockchainCertificate.py -p {0} -cl {1} -noc {2}".format(porttextbox.text(), maxnoofblockstextbox.text() ,noofcertificatestextbox.text()))

        #self.finished.emit()




thread = QThread()
worker = Worker()
worker.moveToThread(thread)
thread.started.connect(worker.run)
worker.finished.connect(thread.quit)
worker.finished.connect(worker.deleteLater)
thread.finished.connect(thread.deleteLater)



class viewblockchain(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI()
                self.setFixedSize(700, 320)
        def initUI(self):
                global data_json
                self.setWindowTitle("View Blockchain")
                icon_path = resource_path('python.ico')
                self.setWindowIcon(QIcon(str(icon_path)))
                horzi = QHBoxLayout(self)

                treeview = QTreeView()
                treeview.setHeaderHidden(True)

                treemodel = QStandardItemModel()
                
                


                rootNode = treemodel.invisibleRootItem()
                transactions = StandardItem('Transactions', 12, set_bold=True)

                # california = StandardItem('California', 14)
                # america.appendRow(california)

                # oakland = StandardItem('Oakland', 12, color=QColor(155, 0, 0))
                # sanfrancisco = StandardItem('San Francisco', 12, color=QColor(155, 0, 0))
                # sanjose = StandardItem('San Jose', 12, color=QColor(155, 0, 0))

                # california.appendRow(oakland)
                # california.appendRow(sanfrancisco)
                # california.appendRow(sanjose)


                # texas = StandardItem('Texas', 14)
                # america.appendRow(texas)

                # austin = StandardItem('Austin', 12, color=QColor(155, 0, 0))
                # houston = StandardItem('Houston', 12, color=QColor(155, 0, 0))
                # dallas = StandardItem('dallas', 12, color=QColor(155, 0, 0))

                # texas.appendRow(austin)
                # texas.appendRow(houston)
                # texas.appendRow(dallas)


                # # Canada 
                # canada = StandardItem('America', 16, set_bold=True)

                # alberta = StandardItem('Alberta', 14)
                # bc = StandardItem('British Columbia', 14)
                # ontario = StandardItem('Ontario', 14)
                # canada.appendRows([alberta, bc, ontario])


                
                # rootNode.appendRow(canada)

               


                # first = StandardItem("first item", 16, set_bold=True)
                # second = StandardItem("first child item", 14)

                # first.appendRow(second)

                # treeview.setModel(treemodel)

                msglabel = QPlainTextEdit(self)
                msglabel.setReadOnly(True)
                msglabel.setFont(QFont('Seoge UI', 10))
                # msglabel.setFixedSize(700, 300)
                # msglabel.setPlainText("")
                # print(str(data_json['chain']))
                # print("LLLLLLLLLLLLLLLLLLLLLLLLL")
                # print(list(data_json['chain'][0]))
                for i in range(int(data_json['length'])):
                        msglabel.appendPlainText('Block '+str(i)+": "+str(data_json['chain'][i])+"\n")

                # viewblockchaindialog.addWidget(horzi)
                
                # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                # for i in range(int(noofcertificatestextbox.text())):
                #         print(i)
                #         print(dict(dict(data_json['chain'][0])['transactions'][i])['certificateName'])
                # # print(dict(data_json['chain'][0])['transactions'])
                # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

                # f = QFile('D:/WORK/Blockchain/default.txt')
                # f.open(QIODevice.ReadOnly)
                # viewlist = ' '.join([str(elem) for elem in list(dict(data_json['chain'][0])['transactions'])])
                # model = TreeModel(viewlist)
                # f.close()
                # model = TreeModel()
                # view = QTreeView(viewblockchaindialog)
                # view.setModel(model)

                print('''
                lllllll
                llllllll
                llllllllllll
                lllllllllllllllllllllllllll''')
                print(data_json['chain'])
                try:
                        for i in range(int(noofcertificatestextbox.text())):
                                print(i)
                                blk = StandardItem('Block '+str(i+1),10,set_bold=True)
                                transactions.appendRow(blk)
                                for j in range(int(noofcertificatestextbox.text())):
                                        blkcode = StandardItem(str(dict(data_json['chain'][i+1])['transactions'][j]['certificateName']),10)
                                        print(dict(data_json['chain'][i+1])['transactions'][j]['certificateName'])
                                        blk.appendRow(blkcode)
                except Exception as e:
                        print("$$$$$$$$$$$$$$$$ ERROR $$$$$$$$$$$$$$$$", e)

                # for i in range(int(data_json['length'])):
                #         blk = StandardItem('Block '+str(i+1),10)
                #         transactions.appendRow(blk)
                #         blkcode = StandardItem(str(dict(data_json['chain'][i]['transactions'])['certificateName']),10)
                #         # print(str(data_json['chain'][i]['transactions']))
                #         blk.appendRow(blkcode)


                print('''
                ooooooo
                oooooooo
                oooooooooooo
                ooooooooooooooooooooooooooo''')


                rootNode.appendRow(transactions)
                treeview.setModel(treemodel)
                treeview.expandAll()
                treeview.doubleClicked.connect(self.getValue)

                horzi.addWidget(msglabel)
                horzi.addWidget(treeview)
                
                self.setLayout(horzi)

        def getValue(self, val):
                print(val.data())
                print(val.row())
                print(val.column())




class MainWindow(QWidget):
        def __init__(self):
                super().__init__()
                self.initUI()
                self.setFixedSize(700, 320)
        def initUI(self):
                global data_json, crypto,connectinglabel,process,activenodescountlabel,noofcertificatestextbox,maxnoofblockstextbox, porttextbox, count, thread, thread1,activenodestext,certificatecountlabel,blockcountlabel, activenodesanslabel
                # self.item = Worker1(myString="mystr")
                # self.item.textboxmsg.connect(self.changedtext)
                #self.worker.progress.connect(self.reportProgress)
                #self.thread.start()

                self.setWindowFlags( Qt.WindowCloseButtonHint |  Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
                self.setWindowTitle('Server Section')
                # self.style().standardIcon(QStyle.SP_DialogOpenButton)
                # desktop_icon = QIcon(QApplication.style().standardIcon(QStyle.SP_DesktopIcon))
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



                startbutton = QPushButton("Start", self)
                startbutton.clicked.connect(self.on_start)
                startbutton.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                startbutton.setFixedHeight(35)

                stopbutton = QPushButton("Stop", self)
                stopbutton.clicked.connect(self.on_stop)
                stopbutton.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
                stopbutton.setFixedHeight(35)

                #self.startbutton.setStyleSheet('QPushButton {  border-color: white; border-width: 1px; padding: 14px; border-style: outset; border-radius: 6px; background-color: #1c9c1e; font-weight:regular;fo>                self.startbutton.setCursor(QCursor(Qt.PointingHandCursor))

                blockchainviewbutton = QPushButton("View Blockchain", self)
                blockchainviewbutton.clicked.connect(self.view_blockchain)
                #self.blockchainviewbutton.setStyleSheet('QPushButton {  border-color: white; border-width: 1px; padding: 14px; border>
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


                noofcertificateslabel = QLabel("No of certificates per block",self)
                noofcertificateslabel.setFixedWidth(200)
                noofcertificateslabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")


                maxnoofblockslabel = QLabel("Max no of blocks",self)
                maxnoofblockslabel.setFixedWidth(200)
                maxnoofblockslabel.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")
            
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
                
                noofcertificatestextbox = QLineEdit(self)
                # noofcertificatestextbox.move(20, 20)
                noofcertificatestextbox.resize(20,20)
                noofcertificatestextbox.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                maxnoofblockstextbox = QLineEdit(self)
                # noofcertificatestextbox.move(20, 20)
                maxnoofblockstextbox.resize(20,20)
                maxnoofblockstextbox.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                porttextbox = QLineEdit(self)
                # noofcertificatestextbox.move(20, 20)
                porttextbox.resize(20,20)
                porttextbox.setStyleSheet("font-weight: regular; font-size: 10pt; font-family: Seoge UI; color: black;")

                # self.livestatustext = QPlainTextEdit(self)
                # self.livestatustext.setReadOnly(True)
                # self.livestatustext.insertPlainText("")
                

                # activenodestext = QPlainTextEdit(self)
                # activenodestext.setReadOnly(True)
                # activenodestext.insertPlainText("")



                


                # vtwolayout.SetFixedSize(600,300)
                #Glayout.addWidget(self.experimentlabel,0,0)
                # Glayout.addWidget(cb,0,0)
                Glayout.addLayout(vtwolayout,0,0)
                # vtwolayout.addWidget(QWidget())
                # vtwolayout.addWidget(self.cb)
                # vtwolayout.addWidget(hframe1)
                vtwolayout.addWidget(livestatuslabel)
                # Glayout.addWidget(self.livestatustext,1,0)
                vtwolayout.addWidget(connectinglabel)
                vtwolayout.addWidget(certificatecountlabel)
                vtwolayout.addWidget(blockcountlabel)
                #Glayout.addWidget(self.livestatuslabel,2,0)
                Glayout.addWidget(vframe,0,1)
                Glayout.addLayout(vonelayout,0,2)
                vonelayout.addWidget(configuretextlabel)


                vonelayout.addLayout(vlayout)
                vlayout.addLayout(honelayout)
                
                honelayout.addWidget(noofcertificateslabel)
                honelayout.addWidget(noofcertificatestextbox)

                vlayout.addLayout(htwolayout)
                htwolayout.addWidget(maxnoofblockslabel)
                htwolayout.addWidget(maxnoofblockstextbox)

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

                hlayout.addWidget(blockchainviewbutton)
                # hlayout.addWidget(walletviewbutton)
                # Glayout.addLayout(hlayout,3,2)

                #vlayout.addWidget(self.experimentlabel)
                #hlayout.addWidget(self.cb)
                self.setLayout(Glayout)


        def selectionchange(self,i):
                global crypto
                for count in range(self.cb.count()):
                        print(self.cb.itemText(count))
                print("Current index", i, "selection changed", self.cb.currentText())
                if self.cb.currentIndexChanged:
                        crypto = QDialog()
                        crypto.setModal(True)
                        crypto.setWindowTitle("Server section")
                        crypto.setFixedSize(700, 300)
                        icon_path = resource_path('python.ico') #os.path.realpath("enablAR.ico") #Path(__file__).parent / "../icons/enablAR.ico"
                        crypto.setWindowIcon(QIcon(str(icon_path)))

                        # Glayout1 = QGridLayout()

                        # crypto.cryptocb = QComboBox()
                        # crypto.cryptocb.addItem("Certificate")
                        # crypto.cryptocb.addItem("Cryptocurrency")
                        # # crypto.cryptocb.currentIndexChanged.connect(crypto.cryptoselectionchange)
                        # crypto.cryptocb.setStyleSheet("font-weight: bold; font-size: 10pt; font-family: Seoge UI; color: black;")


                        # Glayout1.addWidget(crypto.cryptocb)
                        # self.close()
                        
        
                        # def cryptoselectionchange(cryptocb,i):
                        #         for count in range(cryptocb.cb.count()):
                        #                 print(cryptocb.cb.itemText(count))
                        #         print("Current index", i, "selection changed", cryptocb.cb.currentText())
                        
                        crypto.exec_()

        def on_click(self):
                print("clicked")
        def view_blockchain(self):
                global data_json
                print("view blockchain windows")

                try:
                        url = "http://localhost:"+ porttextbox.text() +"/chain"
                        response = urlopen(url)
                        data_json = json.loads(response.read())
                        # print(data_json['chain'])
                except:
                        print("netowrk error")

                self.w = viewblockchain()
                self.w.show()

                
                # viewblockchaindialog = QDialog()
                # viewblockchaindialog.setModal(True)
                # viewblockchaindialog.setWindowTitle("Blockchain section")
                # viewblockchaindialog.setFixedSize(700, 300)
                # icon_path = resource_path('python.ico') #os.path.realpath("enablAR.ico") #Path(__file__).parent / "../icons/enablAR.ico"
                # viewblockchaindialog.setWindowIcon(QIcon(str(icon_path)))

               
                # treeview.doubleClicked.connect(self.getValue)
                # viewblockchaindialog.setCentralWidget(treeview)

                # viewblockchaindialog.exec_()
                # except Exception as e:
                #         print(e)
        
        # def getValue(self, val):
        #         print(val.data())
        #         print(val.row())
        #         print(val.column())

        def on_start(self):
                # self.livestatustext.setPlainText("Live status")
                connectinglabel.setText("Certificate Blockchain \nrunning on port "+porttextbox.text()+"...")
                # count = 0
                try:
                        thread.start()
                except:
                        print("qtext error")
                #os.system("python3 blockchaincertificate.py -p 4000 -cl 10 -noc 3")
                #sleep(1000)
                #url = "http://172.26.156.150:5000/chain"
                #response = urlopen(url)
                #data_json = json.loads(response.read())
                 #print(data_json)
                #self.livestatustext.appendPlainText(str(data_json))
        def on_stop(self):
                # worker.terminate()
                # thread.terminate()
                # thread1.terminate()
                try:
                        for p in all_processes:
                                print(p)
                                p.kill()
                                # thread.exit()
                                # thread1.exit()
                        connectinglabel.setText("Certificate Blockchain \non port "+porttextbox.text()+" \nstopped running...")
                except RuntimeError:
                        print("already deleted")
        def closeEvent(self,event):
                global process
                print("closing application")
                for p in all_processes:
                        p.kill()
                        # thread.exit()
                        # thread1.exit()
                        print ('cleaned up!')
                # process.kill()
                # os.kill(0, signal.SIGKILL)
                # os.system("taskkill /f /im ssf.exe")
                # os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Send the signal to all the process groups

        

def main():
        app=QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()