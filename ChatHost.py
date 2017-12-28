

from PyQt5 import QtCore, QtGui, QtWidgets
import socket
from _thread import *

# Class for GUI created by PyQt5 UI code generator 5.9.1
# Sets up and creates all elements in the GUI
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(396, 230)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.ipInput = QtWidgets.QLineEdit(self.centralwidget)
        self.ipInput.setObjectName("ipInput")
        self.verticalLayout.addWidget(self.ipInput)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.portInput = QtWidgets.QLineEdit(self.centralwidget)
        self.portInput.setObjectName("portInput")
        self.verticalLayout.addWidget(self.portInput)
        self.host = QtWidgets.QPushButton(self.centralwidget)
        self.host.setObjectName("host")
        self.host.clicked.connect(self.hostSocket)
        self.verticalLayout.addWidget(self.host)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.sendMessage = QtWidgets.QPushButton(self.centralwidget)
        self.sendMessage.setObjectName("sendMessage")
        self.sendMessage.clicked.connect(self.sendToClient)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Chat Host"))
        self.label.setText(_translate("MainWindow", "IP Address"))
        self.label_2.setText(_translate("MainWindow", "Host"))
        self.host.setText(_translate("MainWindow", "Host"))
        self.sendMessage.setText(_translate("MainWindow", "Send Message"))

    # Method called when Host button is pressed
    # Creates a new socket object and binds it to the specified IP and Port
    # After socket is bound, it waits for an incoming client connection and then begins listening
    def hostSocket(self):
        hostIP = self.ipInput.text()
        hostPort = int(self.portInput.text())
        sock = socket.socket()

        try:
            sock.bind((hostIP, hostPort))
        except socket.error as e:
            print(str(e))

        sock.listen(1)
        global conn, address
        conn, address = sock.accept()
        self.textEdit.append("Received connection from " + address[0])

        start_new_thread(listen, (conn,))

    # Method called when the Send Message button is pressed
    # Takes message from the user text box and runs the send method on a new thread
    # If "q" is entered as the message, the connection is broken
    def sendToClient(self):
        global message
        message = self.inputBox.toPlainText()
        start_new_thread(send,(conn,))
        if message == 'q':
            self.textEdit.append("Connection closed.")
            self.inputBox.clear()
        else:
            self.textEdit.append("You: " + message)
            self.inputBox.clear()

# Method that sends the message to the client
# Closes connection if message is equal to "q"
def send(conn):
    if message == 'q':
        conn.send("has closed the connection.".encode())
        conn.close()
    else:
        conn.send(message.encode())

# Method that is run as its own thread
# Allows the host to constantly listen for incoming messages
# Will listen until connection is closed
def listen(conn):
    while True:
        incoming = conn.recv(1024)
        if not incoming:
            break
        print("Client: " + incoming.decode())
        ui.textEdit.append("Client: " + incoming.decode())
    conn.close()
    print("Connection closed")

# Main method that initializes and displays the GUI
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

