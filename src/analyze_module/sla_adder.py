from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp, QDateTime, QTime

import qdarkstyle
import time
import pika
import json
import sys


class PopupWindow(QtWidgets.QMainWindow):
    send_fig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(PopupWindow, self).__init__()

        self.parameters = ["oneWayDelay"]

        self.setup_ui()

        self.show()


    def setup_ui(self):

        self.resize(750, 200)
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)


        # Create graph tab
        self.graphTab = QtWidgets.QWidget()
        self.gridLayout_2 = QtWidgets.QGridLayout(self.graphTab)

        self.create_flow_tab()
        self.create_cred_tab()

        self.verticalLayout.addWidget(self.tabWidget)
        self.add_accept_button()
        self.verticalLayout.addWidget(self.graphTab)


        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(self)

    def create_cred_tab(self):
        self.credentialsTab = QtWidgets.QWidget()
        self.credentialsTab.setObjectName("credentialsTab")
        self.verticalLayout10 = QtWidgets.QHBoxLayout(self.credentialsTab)
        self.verticalLayout10.setObjectName("verticalLayout10")
        self.groupBox_16 = QtWidgets.QGroupBox(self.credentialsTab)
        self.groupBox_16.setObjectName("groupBox_16")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_16)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        spacerItem0 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem0)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_14 = QtWidgets.QLabel(self.groupBox_16)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_14.addWidget(self.label_14)
        self.hostnameLine1 = QtWidgets.QLineEdit(self.groupBox_16)
        self.hostnameLine1.setObjectName("hostnameLine1")
        self.verticalLayout_14.addWidget(self.hostnameLine1)
        self.horizontalLayout_14.addLayout(self.verticalLayout_14)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.groupBox_16)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_13.addWidget(self.label_13)
        self.portBox1 = QtWidgets.QSpinBox(self.groupBox_16)
        self.portBox1.setMaximum(50000)
        self.portBox1.setProperty("value", 5672)
        self.portBox1.setObjectName("portBox1")
        self.verticalLayout_13.addWidget(self.portBox1)
        self.horizontalLayout_14.addLayout(self.verticalLayout_13)
        self.verticalLayout_10.addLayout(self.horizontalLayout_14)
        spacerItem01 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem01)
        self.verticalLayout10.addWidget(self.groupBox_16)
        spacerItem02 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout10.addItem(spacerItem02)
        self.groupBox_15 = QtWidgets.QGroupBox(self.credentialsTab)
        self.groupBox_15.setObjectName("groupBox_15")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.groupBox_15)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        spacerItem03 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_15.addItem(spacerItem03)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label10 = QtWidgets.QLabel(self.groupBox_15)
        self.label10.setMinimumSize(QtCore.QSize(70, 0))
        self.label10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label10.setObjectName("label10")
        self.horizontalLayout_12.addWidget(self.label10)
        self.usernameLine1 = QtWidgets.QLineEdit(self.groupBox_15)
        self.usernameLine1.setObjectName("usernameLine1")
        self.horizontalLayout_12.addWidget(self.usernameLine1)
        spacerItem04 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem04)
        self.verticalLayout_15.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_12 = QtWidgets.QLabel(self.groupBox_15)
        self.label_12.setMinimumSize(QtCore.QSize(70, 0))
        self.label_12.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_13.addWidget(self.label_12)
        self.passwordLine1 = QtWidgets.QLineEdit(self.groupBox_15)
        self.passwordLine1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine1.setObjectName("passwopasswordLine1rdLine")
        self.horizontalLayout_13.addWidget(self.passwordLine1)
        spacerItem05 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem05)
        self.verticalLayout_15.addLayout(self.horizontalLayout_13)
        spacerItem06 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_15.addItem(spacerItem06)
        self.verticalLayout10.addWidget(self.groupBox_15)
        spacerItem07 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout10.addItem(spacerItem07)
        self.tabWidget.addTab(self.credentialsTab, "")

    def add_accept_button(self):
        """ Function that add ADD and DELETE buttons to the User Interface """

        # ADD button
        buttonText = 'ADD'
        self.button = QPushButton(buttonText)

        width = self.button.fontMetrics().boundingRect(buttonText).width() + 20
        self.button.setMaximumWidth(width)
        self.button.clicked.connect(lambda: self.update("ADD"))

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.button, 0, QtCore.Qt.AlignRight)

        self.verticalLayout.addLayout(self.hbox)

        # DELETE button
        buttonText2 = 'DELETE'
        self.button2 = QPushButton(buttonText2)
        width = self.button2.fontMetrics().boundingRect(buttonText2).width() + 20
        self.button2.setMaximumWidth(width)
        self.hbox.addWidget(self.button2, 0, QtCore.Qt.AlignLeft)
        self.button2.clicked.connect(lambda: self.update("DELETE"))
        self.enable_button()

    def enable_button(self, variableName = None, value = None):
        """ Enabling ADD and DELETE buttons only when the IP addresses are
            correct """

        if variableName is not None and value is not None:
            setattr(self, variableName, value)

        enable = self.ipSrcCorrect and \
                 self.ipDstCorrect

        self.button.setEnabled(enable)
        self.button2.setEnabled(enable)

    def update(self, text):
        """ Sending the update message to the server """

        flow = self.ipDstLineEdit.text()+"."+self.ipSrcLineEdit.text()+"."+ \
               self.portDstLineEdit.text()+"."+self.portSrcLineEdit.text()+"."+ \
               self.protocolLineEdit.text()

        msg = {"delay" : {"warning" : self.warn.text(), "alert" : self.al.text()}, "flow" : flow, "action" : text}

        self.send(json.dumps(msg).encode())

    def send(self, msg):

        routingkey = "SLA.server"
        exchange = "topic_logs3"
        type = "topic"

        host = self.hostnameLine1.text()
        port = self.portBox1.value()
        login = self.usernameLine1.text()
        password = self.passwordLine1.text()

        try:
            credentials = pika.PlainCredentials(login, password)
            params = pika.connection.ConnectionParameters(host, int(port), "/", credentials)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange, exchange_type=type)

            try:
                channel.basic_publish(exchange=exchange, routing_key=routingkey, body=msg)
            except pika.exceptions.ConnectionClosed:
                print("The connection was down.")

            if connection and connection.is_open:
                connection.close()
        except Exception:
            pass

    def create_flow_tab(self):
        """Create flow tab"""

        self.flowTab = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.flowTab)
        self.groupBox = QtWidgets.QGroupBox(self.flowTab)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()


        # Add IPv4 Source Address Line Edit
        self.ipSrcLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.horizontalLayout.addWidget(self.ipSrcLineEdit)
        self.ipSrcCorrect = False
        ipv4Regex = QRegExp("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        self.ipSrcLineEdit.textChanged.connect(lambda x: self.enable_button('ipSrcCorrect', True) if ipv4Regex.exactMatch(x) else  self.enable_button('ipSrcCorrect', False))


        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.verticalLayout_2.addWidget(self.label_2)

        # Add Source Port Line Edit
        self.portSrcLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.verticalLayout_2.addWidget(self.portSrcLineEdit)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.flowTab)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()

        # Add IPv4 Destination Address Line Edit
        self.ipDstLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.ipDstCorrect = False
        self.horizontalLayout_2.addWidget(self.ipDstLineEdit)
        self.ipDstLineEdit.textChanged.connect(lambda x: self.enable_button('ipDstCorrect', True) if ipv4Regex.exactMatch(x) else  self.enable_button('ipDstCorrect', False))


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.verticalLayout_3.addWidget(self.label_4)

        # Add Destination Port Line Edit
        self.portDstLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.verticalLayout_3.addWidget(self.portDstLineEdit)

        self.gridLayout.addWidget(self.groupBox_2, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.flowTab)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.line, 0, 1, 1, 1)

        self.groupBox_6 = QtWidgets.QGroupBox(self.flowTab)
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_6)
        self.label_5 = QtWidgets.QLabel(self.groupBox_6)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)

        self.protocolLineEdit = QtWidgets.QLineEdit(self.groupBox_6)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.protocolLineEdit)

        self.gridLayout.addWidget(self.groupBox_6, 0, 4, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.flowTab)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.line_2, 0, 3, 1, 1)
        self.tabWidget.addTab(self.flowTab, "")


        self.groupBox_3 = QtWidgets.QGroupBox(self.flowTab)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.labelX = QtWidgets.QLabel(self.groupBox_3)
        self.verticalLayout_4.addWidget(self.labelX)
        self.horizontalLayout = QtWidgets.QHBoxLayout()


        self.warn = QtWidgets.QLineEdit(self.groupBox_3)
        self.horizontalLayout.addWidget(self.warn)

        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.labelY = QtWidgets.QLabel(self.groupBox_3)
        self.verticalLayout_4.addWidget(self.labelY)

        self.al = QtWidgets.QLineEdit(self.groupBox_3)
        self.verticalLayout_4.addWidget(self.al)

        self.gridLayout.addWidget(self.groupBox_3, 0, 5, 1, 1)

        self.add_flow_validators()


    def add_flow_validators(self):


        # Validate source and destination IPv4 addresses
        ipv4Regex = QRegExp("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        ipv4Validator = QRegExpValidator(ipv4Regex)
        self.ipDstLineEdit.setValidator(ipv4Validator)
        self.ipSrcLineEdit.setValidator(ipv4Validator)

        # Validate protocol number (0-255)
        self.protocolLineEdit.setValidator(QIntValidator(0,255))
        self.protocolLineEdit.setMaxLength(3)

        # Validate port numbers (0-65535)
        self.portSrcLineEdit.setValidator(QIntValidator(0,65535))
        self.portSrcLineEdit.setMaxLength(5)
        self.portDstLineEdit.setValidator(QIntValidator(0,65535))
        self.portDstLineEdit.setMaxLength(5)

        valRegex = QRegExp("^([0-9])+$")
        valValidator = QRegExpValidator(valRegex)
        self.warn.setValidator(valValidator)
        self.al.setValidator(valValidator)


    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PopupWindow", "Edit SLA values"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Specify the server you want to connect to"))
        self.label_14.setText(_translate("MainWindow", "Host Name (or IP address)"))
        self.label_13.setText(_translate("MainWindow", "Port"))
        self.groupBox_15.setTitle(_translate("MainWindow", "Credentials"))
        self.label10.setText(_translate("MainWindow", "Username"))
        self.label_12.setText(_translate("MainWindow", "Password"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.credentialsTab), _translate("PopupWindow", "Credentials"))
        self.groupBox.setTitle(_translate("PopupWindow", "Source"))
        self.label.setText(_translate("PopupWindow", "IP address"))
        self.label_2.setText(_translate("PopupWindow", "Port"))
        self.groupBox_2.setTitle(_translate("PopupWindow", "Destination"))
        self.label_3.setText(_translate("PopupWindow", "IP address"))
        self.label_4.setText(_translate("PopupWindow", "Port"))
        self.labelX.setText(_translate("PopupWindow", "Warning delay"))
        self.labelY.setText(_translate("PopupWindow", "Alert delay"))
        self.groupBox_6.setTitle(_translate("PopupWindow", "Protocol"))
        self.label_5.setText(_translate("PopupWindow", "Protocol number"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.flowTab), _translate("PopupWindow", "Flow parameters"))
        self.groupBox_16.setTitle(_translate("PopupWindow", "Server"))
