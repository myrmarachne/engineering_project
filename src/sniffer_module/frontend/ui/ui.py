# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Wed Aug 16 10:03:31 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import json
import re
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 450)
        MainWindow.setMinimumSize(QtCore.QSize(408, 412))
        MainWindow.setMaximumSize(QtCore.QSize(480, 507))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(462, 375))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.hostnameLine = QtWidgets.QLineEdit(self.groupBox_4)
        self.hostnameLine.setObjectName("hostnameLine")
        self.verticalLayout_4.addWidget(self.hostnameLine)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.portBox = QtWidgets.QSpinBox(self.groupBox_4)
        self.portBox.setMaximum(50000)
        self.portBox.setProperty("value", 3306)
        self.portBox.setObjectName("portBox")
        self.verticalLayout_3.addWidget(self.portBox)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_5)
        self.label.setMinimumSize(QtCore.QSize(70, 0))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.usernameLine = QtWidgets.QLineEdit(self.groupBox_5)
        self.usernameLine.setObjectName("usernameLine")
        self.horizontalLayout_2.addWidget(self.usernameLine)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_5)
        self.label_2.setMinimumSize(QtCore.QSize(70, 0))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.passwordLine = QtWidgets.QLineEdit(self.groupBox_5)
        self.passwordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLine.setObjectName("passwordLine")
        self.horizontalLayout_3.addWidget(self.passwordLine)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem6)
        self.verticalLayout.addWidget(self.groupBox_5)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.databaseLine = QtWidgets.QLineEdit(self.groupBox_2)
        self.databaseLine.setObjectName("databaseLine")
        self.verticalLayout_7.addWidget(self.databaseLine)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.verticalLayout_7)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.LabelRole, spacerItem8)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(2, QtWidgets.QFormLayout.LabelRole, spacerItem9)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_9.addWidget(self.label_8)
        self.interfacesBox = QtWidgets.QComboBox(self.groupBox_3)
        self.interfacesBox.setObjectName("interfacesBox")
        self.verticalLayout_9.addWidget(self.interfacesBox)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem10)
        self.gridLayout_3.addLayout(self.verticalLayout_9, 1, 2, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem11, 1, 1, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem12, 0, 0, 1, 1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.timeoutEdit = QtWidgets.QTimeEdit(self.groupBox_3)
        self.timeoutEdit.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.timeoutEdit.setObjectName("timeoutEdit")
        self.verticalLayout_8.addWidget(self.timeoutEdit)
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.bufferSizeBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.bufferSizeBox.setObjectName("bufferSizeBox")
        self.verticalLayout_8.addWidget(self.bufferSizeBox)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem13)
        self.gridLayout_3.addLayout(self.verticalLayout_8, 1, 0, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem14, 2, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.tabWidget.addTab(self.tab_2, "")


        self.tab3 = QtWidgets.QWidget()
        self.tab3.setObjectName("tab3")
        self.verticalLayout10 = QtWidgets.QVBoxLayout(self.tab3)
        self.verticalLayout10.setObjectName("verticalLayout10")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab3)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        spacerItem0 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem0)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_14 = QtWidgets.QLabel(self.groupBox_6)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_14.addWidget(self.label_14)
        self.hostnameLine1 = QtWidgets.QLineEdit(self.groupBox_6)
        self.hostnameLine1.setObjectName("hostnameLine1")
        self.verticalLayout_14.addWidget(self.hostnameLine1)
        self.horizontalLayout_14.addLayout(self.verticalLayout_14)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_13 = QtWidgets.QLabel(self.groupBox_6)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_13.addWidget(self.label_13)
        self.portBox1 = QtWidgets.QSpinBox(self.groupBox_6)
        self.portBox1.setMaximum(50000)
        self.portBox1.setProperty("value", 5672)
        self.portBox1.setObjectName("portBox1")
        self.verticalLayout_13.addWidget(self.portBox1)
        self.horizontalLayout_14.addLayout(self.verticalLayout_13)
        self.verticalLayout_10.addLayout(self.horizontalLayout_14)
        spacerItem01 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem01)
        self.verticalLayout10.addWidget(self.groupBox_6)
        spacerItem02 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout10.addItem(spacerItem02)
        self.groupBox_15 = QtWidgets.QGroupBox(self.tab3)
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
        self.tabWidget.addTab(self.tab3, "")


        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem15)
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setObjectName("connectButton")
        self.horizontalLayout.addWidget(self.connectButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Specify the database you want to connect to"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Specify the server you want to connect to"))
        self.label_4.setText(_translate("MainWindow", "Host Name (or IP address)"))
        self.label_14.setText(_translate("MainWindow", "Host Name (or IP address)"))
        self.label_3.setText(_translate("MainWindow", "Port"))
        self.label_13.setText(_translate("MainWindow", "Port"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Credentials"))
        self.groupBox_15.setTitle(_translate("MainWindow", "Credentials"))
        self.label10.setText(_translate("MainWindow", "Username"))
        self.label.setText(_translate("MainWindow", "Username"))
        self.label_12.setText(_translate("MainWindow", "Password"))
        self.label_2.setText(_translate("MainWindow", "Password"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Database"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Database Connection"))
        self.label_5.setText(_translate("MainWindow", "Database"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Sniffer"))
        self.label_8.setText(_translate("MainWindow", "Select interface for sniffing"))
        self.label_6.setText(_translate("MainWindow", "Timeout"))
        self.timeoutEdit.setDisplayFormat(_translate("MainWindow", "HH:mm:ss"))
        self.label_7.setText(_translate("MainWindow", "Maximum Buffer Size"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Preferences"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), _translate("MainWindow", "Server"))

    def addCallbacks(self, MainWindow):
        MainWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.connectButton.clicked.connect(lambda: self.connectButtonCallback(MainWindow))
        self.interfacesBox.activated.connect(self.handleInterfacesBox)

    def addInterfaces(self, interfaces):
        for int in interfaces:
            self.interfacesBox.addItem(int)

    def handleInterfacesBox(self):
        self.Interface = str(self.interfacesBox.currentText())

    def connectButtonCallback(self, MainWindow):
        # extract data from form
        params = {}
        params["DataBaseConnector"] = {}
        params["MeasureData"] = {}
        params["SLAConnectionHandler"] = {}

        params["DataBaseConnector"]["HOSTNAME"] = self.hostnameLine.text()
        params["DataBaseConnector"]["USERNAME"] = self.usernameLine.text()
        params["DataBaseConnector"]["PASSWORD"] = self.passwordLine.text()
        params["DataBaseConnector"]["DATABASE"] = self.databaseLine.text()
        params["DataBaseConnector"]["PORT_NO"] = self.portBox.value()

        scriptPath = self.json.filename
        filename = os.path.basename(scriptPath)
        directory = re.sub(filename+'$', '', scriptPath)
        params["DataBaseConnector"]["TABLES"] = {}
        params["DataBaseConnector"]["TABLES"]["Measurments"] = os.path.join(directory, "tables", "measurments.txt")
        params["DataBaseConnector"]["TABLES"]["Applications"] = os.path.join(directory, "tables", "applications.txt")
        params["DataBaseConnector"]["TABLES"]["Options"] = os.path.join(directory, "tables", "options.txt")


        params["MeasureData"]["MAX_SIZE"] = self.bufferSizeBox.value()
        timeout = self.timeoutEdit.time()
        params["MeasureData"]["HOURS"] = timeout.hour()
        params["MeasureData"]["MINUTES"] = timeout.minute()
        params["MeasureData"]["SECONDS"] = timeout.second()

        params["SLAConnectionHandler"]["HOSTNAME"] = self.hostnameLine1.text()
        params["SLAConnectionHandler"]["USERNAME"] = self.usernameLine1.text()
        params["SLAConnectionHandler"]["PASSWORD"] = self.passwordLine1.text()
        params["SLAConnectionHandler"]["PORT"] = self.portBox1.value()

        self.handleInterfacesBox()

        params["Interface"] = self.Interface

        # write data to json file
        self.json.writeToJson(params)
        MainWindow.close()

    def addJsonHandler(self, json):
        self.json = json

class JsonHandler:
    def __init__(self, filename):
        self.filename = filename

    def writeToJson(self, params):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)

                for p in params:
                    if type(params[p]) is dict:
                        for pp in params[p]:
                            data[p][pp] = params[p][pp]
                    elif type(params[p]) is str:
                        data[p] = params[p]

        except Exception:
            with open(self.filename, 'w') as f:
                data = {"DataBaseConnector" : {}, "SLAConnectionHandler" : {}, "MeasureData" : {}}
                for p in params:
                    if type(params[p]) is dict:
                        for pp in params[p]:
                            data[p][pp] = params[p][pp]
                    elif type(params[p]) is str:
                        data[p] = params[p]
                f.write(json.dumps(data))



        with open(self.filename, 'w') as f:
            json.dump(data, f)
