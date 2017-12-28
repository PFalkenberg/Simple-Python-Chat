

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
from _thread import *
from threading import Thread

# Class for GUI created by PyQt5 UI code generator 5.9.1
# Sets up and creates all elements in the GUI
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(398, 230)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(118, 16777215))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.ipInput = QtWidgets.QLineEdit(self.centralwidget)
        self.ipInput.setMaximumSize(QtCore.QSize(123, 16777215))
        self.ipInput.setObjectName("ipInput")
        self.verticalLayout.addWidget(self.ipInput)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(118, 16777215))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.portInput = QtWidgets.QLineEdit(self.centralwidget)
        self.portInput.setMaximumSize(QtCore.QSize(123, 16777215))
        self.portInput.setObjectName("portInput")
        self.verticalLayout.addWidget(self.portInput)
        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setMaximumSize(QtCore.QSize(123, 23))
        self.connect.setObjectName("connect")
        self.connect.clicked.connect(self.connectToHost)
        self.verticalLayout.addWidget(self.connect)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.sendMessage = QtWidgets.QPushButton(self.centralwidget)
        self.sendMessage.setMaximumSize(QtCore.QSize(125, 16777215))
        self.sendMessage.setObjectName("sendMessage")
        self.sendMessage.clicked.connect(self.sendToHost)
        self.gridLayout.addWidget(self.sendMessage, 1, 0, 1, 1)
        self.inputBox = QtWidgets.QTextEdit(self.centralwidget)
        self.inputBox.setObjectName("inputBox")
        self.gridLayout.addWidget(self.inputBox, 1, 1, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat Client"))
        self.label.setText(_translate("MainWindow", "IP Address"))
        self.label_2.setText(_translate("MainWindow", "Host"))
        self.connect.setText(_translate("MainWindow", "Connect"))
        self.sendMessage.setText(_translate("MainWindow", "Send Message"))

    # Method that is called when the connect button is pressed
    # Creates a new socket object and connects it to the specified IP and Port
    # After connecting, it creates a new thread to listen for incoming messages
    def connectToHost(self):
        hostIP = self.ipInput.text()
        hostPort = int(self.portInput.text())
        global sock
        sock = socket.socket()

        try:
            sock.connect((hostIP, hostPort))
        except socket.error as e:
            print(str(e))

        self.textEdit.setText("Connected to host.")

        start_new_thread(listen,())

    # Method called when the send message button is pressed
    # Takes message from text box and calls the send method as a new thread
    def sendToHost(self):
        message = self.inputBox.toPlainText()
        threadSend = Thread(target = send(message))
        threadSend.start()
        if message == 'q':
            self.textEdit.append("Connection closed.")
        else:
            self.textEdit.append("You: " + message)
            self.inputBox.clear()

# Sends the message to the host
# Called from the sendToHost method above
def send(message):
    if message == 'q':
        sock.send("has closed the connection.".encode())
        sock.close()
        print("Connection closed.")
    else:
        sock.send(message.encode())
        print("You: " + message)

# Method that is run as a thread above
# Allows client to constantly listen for incoming messages
def listen():
    while True:
        incoming = sock.recv(1024).decode()
        print("Server: " + incoming)
        ui.textEdit.append("Host: " + incoming)

# Main method that initializes and displays the GUI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

