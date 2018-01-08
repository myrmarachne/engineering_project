from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp, QDateTime, QTime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib import rcParams
from matplotlib.ticker import FormatStrFormatter

from sla_adder import PopupWindow

import sys
import MySQLdb
import qdarkstyle
import time
import pandas as pd


class MainWindow(QtWidgets.QMainWindow):
    send_fig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        # In case of adding new parameters the below list shoul be extended
        self.parameters = ["oneWayDelay"]

        self.timeDeltaFigures = []
        self.amountOfTimedelta = 0
        self.timeDeltaAxes = []
        self.timedeltaTabs = []

        self.dataProvider = DataProvider()

        rcParams.update({'font.size': 6})

        # Setting up the User Interface
        self.setup_ui()

        self.show()


    def setup_ui(self):
        """ Function which creates the Usr Interface with all neede elements
        that must be shown """

        # Resizing the whole application window
        self.resize(685, 573)
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)

        # Creating the graph tab (for the specified parameter - in this case it
        # is the oneWayDelay parameter)

        self.graphTab = QtWidgets.QWidget()
        self.gridLayout_2 = QtWidgets.QGridLayout(self.graphTab)

        self.groupBox_5 = QtWidgets.QGroupBox(self.graphTab)
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_5)

        # Creating the upper tabs with editable fields for parameters of the
        # graph

        self.create_flow_tab()
        self.create_time_tab()
        self.add_db_connection_tab()

        self.verticalLayout.addWidget(self.tabWidget)
        self.add_accept_button()
        self.verticalLayout.addWidget(self.graphTab)


        self.plotTab = QtWidgets.QTabWidget(self.centralwidget)
        self.verticalLayout.addWidget(self.plotTab)
        self.create_plot_tabs()

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 569, 25))
        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.retranslate_ui()
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(self)

    def add_accept_button(self):
        buttonText = 'Submit data'
        self.button = QPushButton(buttonText)

        width = self.button.fontMetrics().boundingRect(buttonText).width() + 20
        self.button.setMaximumWidth(width)
        self.button.clicked.connect(self.update)
        self.enable_button()
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.button, 0, QtCore.Qt.AlignRight)

        self.verticalLayout.addLayout(self.hbox)

        buttonText2 = 'Edit SLA values'
        self.button2 = QPushButton(buttonText2)
        width = self.button2.fontMetrics().boundingRect(buttonText2).width() + 20
        self.button2.setMaximumWidth(width)
        self.hbox.addWidget(self.button2, 0, QtCore.Qt.AlignLeft)
        self.button2.clicked.connect(self.run)

    def run(self):
        win = PopupWindow()
        win.show()

    def enable_button(self, variableName = None, value = None):
        if variableName is not None and value is not None:
            setattr(self, variableName, value)

        enable = self.ipSrcCorrect and \
                 self.ipDstCorrect and \
                 self.timeChange and \
                 self.dateChange and \
                 self.maskSrcCorrect and \
                 self.maskDstCorrect and \
                 self.hostnameCorrect and \
                 self.usernameCorrect

        self.button.setEnabled(enable)

    def create_plot_tabs(self):
        """Create plots"""

        self.owdFigure = Figure()
        self.axOWD = self.owdFigure.add_subplot(111)
        self.canvas2 = FigureCanvas(self.owdFigure)
        self.canvas2.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)
        self.canvas2.setMinimumSize(QtCore.QSize(500, 300))
        self.canvas2.setMaximumSize(QtCore.QSize(10000, 400))
        self.canvas2.updateGeometry()

        self.owdTab = QtWidgets.QWidget()
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(self.canvas2)
        self.owdTab.setLayout(layout2)
        self.plotTab.addTab(self.owdTab, "One Way Delay")

    def add_db_connection_tab(self):
        self.dbTab = QtWidgets.QWidget()

        self.gridLayoutDB = QtWidgets.QGridLayout(self.dbTab)
        self.groupBoxHostDB = QtWidgets.QGroupBox(self.dbTab)
        self.verticalLayoutdbTab = QtWidgets.QVBoxLayout(self.groupBoxHostDB)

        spacerItemDB = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.verticalLayoutdbTab.addItem(spacerItemDB)

        self.labelHostname = QtWidgets.QLabel(self.groupBoxHostDB)
        self.verticalLayoutdbTab.addWidget(self.labelHostname)
        self.horizontalLayoutDB = QtWidgets.QHBoxLayout()

        self.hostnameLineEdit = QtWidgets.QLineEdit(self.groupBoxHostDB)
        self.horizontalLayoutDB.addWidget(self.hostnameLineEdit)
        self.hostnameCorrect = False
        self.hostnameLineEdit.textChanged.connect(lambda x: self.enable_button('hostnameCorrect', True) if len(self.hostnameLineEdit.text()) > 0 else self.enable_button('hostnameCorrect', False))

        self.verticalLayoutdbTab.addLayout(self.horizontalLayoutDB)
        self.labelDatabase = QtWidgets.QLabel(self.groupBoxHostDB)
        self.verticalLayoutdbTab.addWidget(self.labelDatabase)

        self.databaseLineEdit = QtWidgets.QLineEdit(self.groupBoxHostDB)
        self.verticalLayoutdbTab.addWidget(self.databaseLineEdit)

        self.gridLayoutDB.addWidget(self.groupBoxHostDB, 0, 0, 1, 1)
        self.groupBoxCredentials = QtWidgets.QGroupBox(self.dbTab)
        self.verticalLayoutCredentials = QtWidgets.QVBoxLayout(self.groupBoxCredentials)
        spacerItemCredentials = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutCredentials.addItem(spacerItemCredentials)
        self.labelUsername = QtWidgets.QLabel(self.groupBoxCredentials)
        self.verticalLayoutCredentials.addWidget(self.labelUsername)
        self.horizontalLayoutCredentials = QtWidgets.QHBoxLayout()

        self.usernameLineEdit = QtWidgets.QLineEdit(self.groupBoxCredentials)
        self.usernameCorrect = False
        self.horizontalLayoutCredentials.addWidget(self.usernameLineEdit)
        self.usernameLineEdit.textChanged.connect(lambda x: self.enable_button('usernameCorrect', True) if len(self.usernameLineEdit.text()) > 0 else self.enable_button('usernameCorrect', False))

        self.verticalLayoutCredentials.addLayout(self.horizontalLayoutCredentials)
        self.labelPassword = QtWidgets.QLabel(self.groupBoxCredentials)
        self.verticalLayoutCredentials.addWidget(self.labelPassword)

        self.passwordLineEdit = QtWidgets.QLineEdit(self.groupBoxCredentials)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayoutCredentials.addWidget(self.passwordLineEdit)

        self.gridLayoutDB.addWidget(self.groupBoxCredentials, 0, 2, 1, 1)
        self.lineGroupHostCred = QtWidgets.QFrame(self.dbTab)
        self.lineGroupHostCred.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineGroupHostCred.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayoutDB.addWidget(self.lineGroupHostCred, 0, 1, 1, 1)
        self.groupBoxPortDB = QtWidgets.QGroupBox(self.dbTab)
        self.formLayoutProtocol = QtWidgets.QFormLayout(self.groupBoxPortDB)
        self.labelDBPort = QtWidgets.QLabel(self.groupBoxPortDB)
        self.formLayoutProtocol.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelDBPort)

        self.dbPortLineEdit = QtWidgets.QLineEdit(self.groupBoxPortDB)
        self.dbPortLineEdit.setText("3306");
        self.formLayoutProtocol.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.dbPortLineEdit)

        self.gridLayoutDB.addWidget(self.groupBoxPortDB, 0, 4, 1, 1)
        self.lineGroupCredProt = QtWidgets.QFrame(self.dbTab)
        self.lineGroupCredProt.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineGroupCredProt.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayoutDB.addWidget(self.lineGroupCredProt, 0, 3, 1, 1)
        self.tabWidget.addTab(self.dbTab, "")

        # Validate port number of database connection
        self.dbPortLineEdit.setValidator(QIntValidator(0,65535))
        self.dbPortLineEdit.setMaxLength(5)

    def add_timedelta_tab(self, swNumber):

        self.amountOfTimedelta = self.amountOfTimedelta + 1
        number = self.amountOfTimedelta

        figure = Figure()
        self.timeDeltaFigures.append(figure)


        ax = figure.add_subplot(111)
        self.timeDeltaAxes.append(ax)

        canvas = FigureCanvas(figure)
        canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)
        canvas.setMinimumSize(QtCore.QSize(500, 300))
        canvas.setMaximumSize(QtCore.QSize(10000, 400))
        canvas.updateGeometry()

        tab = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(canvas)

        tab.setLayout(layout)
        self.plotTab.addTab(tab, " Timedelta - switch " + str(swNumber)+" ")
        self.timedeltaTabs.append(tab)


    def create_flow_tab(self):
        """ Create flow tab with editable fields, which identify flows according
            to 5 parameters - source IP addres, destination IP addres, source
            port number, destination port number and protocol number. """

        self.flowTab = QtWidgets.QWidget()

        self.gridLayout = QtWidgets.QGridLayout(self.flowTab)
        self.groupBoxSource = QtWidgets.QGroupBox(self.flowTab)
        self.verticalLayoutFlowTab = QtWidgets.QVBoxLayout(self.groupBoxSource)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.verticalLayoutFlowTab.addItem(spacerItem)

        self.labelSourceIPaddress = QtWidgets.QLabel(self.groupBoxSource)
        self.verticalLayoutFlowTab.addWidget(self.labelSourceIPaddress)
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        def set_default_mask(ip, mask):
            try:
                ipLineEdit = getattr(self, ip)
                maskLineEdit = getattr(self, mask)

                firstOctet = int(ipLineEdit.text().split('.', 1)[0])
                if 0 <= firstOctet  <= 127:
                    maskLineEdit.setText("8")
                elif 128 <= firstOctet <= 191:
                    maskLineEdit.setText("16")
                elif 192 <= firstOctet <= 224:
                    maskLineEdit.setText("24")
                self.ipSrcCorrect = True
            except ValueError:
                pass


        # Add IPv4 Source Address Line Edit
        self.ipSrcLineEdit = QtWidgets.QLineEdit(self.groupBoxSource)
        self.horizontalLayout.addWidget(self.ipSrcLineEdit)
        self.srcMaskSet = False
        self.ipSrcCorrect = False
        self.ipSrcLineEdit.editingFinished.connect(lambda: set_default_mask("ipSrcLineEdit", "maskSrcLineEdit") if not self.srcMaskSet else None)
        ipv4Regex = QRegExp("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        self.ipSrcLineEdit.textChanged.connect(lambda x: self.enable_button('ipSrcCorrect', True) if ipv4Regex.exactMatch(x) else  self.enable_button('ipSrcCorrect', False))

        # Add Source Mask Line Edit
        self.maskSrcLineEdit = QtWidgets.QLineEdit(self.groupBoxSource)
        self.maskSrcLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.maskSrcLineEdit.editingFinished.connect(lambda: setattr(self, 'srcMaskSet', True))
        self.maskSrcCorrect = False
        self.maskSrcLineEdit.textChanged.connect(lambda x: self.enable_button('maskSrcCorrect', len(x)>0))
        self.horizontalLayout.addWidget(self.maskSrcLineEdit)

        self.verticalLayoutFlowTab.addLayout(self.horizontalLayout)
        self.labelSourcePort = QtWidgets.QLabel(self.groupBoxSource)
        self.verticalLayoutFlowTab.addWidget(self.labelSourcePort)

        # Add Source Port Line Edit
        self.portSrcLineEdit = QtWidgets.QLineEdit(self.groupBoxSource)
        self.verticalLayoutFlowTab.addWidget(self.portSrcLineEdit)

        self.gridLayout.addWidget(self.groupBoxSource, 0, 0, 1, 1)
        self.groupBoxDestination = QtWidgets.QGroupBox(self.flowTab)
        self.verticalLayoutDestination = QtWidgets.QVBoxLayout(self.groupBoxDestination)
        spacerItemDestination = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutDestination.addItem(spacerItemDestination)
        self.labelDestinationIPaddress = QtWidgets.QLabel(self.groupBoxDestination)
        self.verticalLayoutDestination.addWidget(self.labelDestinationIPaddress)
        self.horizontalLayoutDestination = QtWidgets.QHBoxLayout()

        # Add IPv4 Destination Address Line Edit
        self.ipDstLineEdit = QtWidgets.QLineEdit(self.groupBoxDestination)
        self.ipDstCorrect = False
        self.horizontalLayoutDestination.addWidget(self.ipDstLineEdit)
        self.dstMaskSet = False
        self.ipDstLineEdit.editingFinished.connect(lambda: set_default_mask("ipDstLineEdit", "maskDstLineEdit") if not self.dstMaskSet else None)
        self.ipDstLineEdit.textChanged.connect(lambda x: self.enable_button('ipDstCorrect', True) if ipv4Regex.exactMatch(x) else  self.enable_button('ipDstCorrect', False))

        # Add Destination Mask Line Edit
        self.maskDstLineEdit = QtWidgets.QLineEdit(self.groupBoxDestination)
        self.maskDstLineEdit.editingFinished.connect(lambda: setattr(self, 'dstMaskSet', True))
        self.maskDstCorrect = False
        self.maskDstLineEdit.textChanged.connect(lambda x: self.enable_button('maskDstCorrect', len(x)>0))
        self.maskDstLineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.horizontalLayoutDestination.addWidget(self.maskDstLineEdit)

        self.verticalLayoutDestination.addLayout(self.horizontalLayoutDestination)
        self.labelDestinationPort = QtWidgets.QLabel(self.groupBoxDestination)
        self.verticalLayoutDestination.addWidget(self.labelDestinationPort)

        # Add Destination Port Line Edit
        self.portDstLineEdit = QtWidgets.QLineEdit(self.groupBoxDestination)
        self.verticalLayoutDestination.addWidget(self.portDstLineEdit)

        self.gridLayout.addWidget(self.groupBoxDestination, 0, 2, 1, 1)
        self.lineGroupSrcDst = QtWidgets.QFrame(self.flowTab)
        self.lineGroupSrcDst.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineGroupSrcDst.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.lineGroupSrcDst, 0, 1, 1, 1)
        self.groupBoxProtocol = QtWidgets.QGroupBox(self.flowTab)
        self.formLayoutProtocol = QtWidgets.QFormLayout(self.groupBoxProtocol)
        self.labelProtocol = QtWidgets.QLabel(self.groupBoxProtocol)
        self.formLayoutProtocol.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelProtocol)

        self.protocolLineEdit = QtWidgets.QLineEdit(self.groupBoxProtocol)
        self.formLayoutProtocol.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.protocolLineEdit)

        self.gridLayout.addWidget(self.groupBoxProtocol, 0, 4, 1, 1)
        self.lineGroupDstProtol = QtWidgets.QFrame(self.flowTab)
        self.lineGroupDstProtol.setFrameShape(QtWidgets.QFrame.VLine)
        self.lineGroupDstProtol.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.lineGroupDstProtol, 0, 3, 1, 1)
        self.tabWidget.addTab(self.flowTab, "")

        # Add validators for flow parameters input
        self.add_flow_validators()


    def add_flow_validators(self):
        """ Validate the inputs for flow parameters """

        # Validate source and destination masks (only integers, 0-32)
        self.maskSrcLineEdit.setValidator(QIntValidator(0,32))
        self.maskSrcLineEdit.setMaxLength(2)
        self.maskDstLineEdit.setValidator(QIntValidator(0,32))
        self.maskDstLineEdit.setMaxLength(2)

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



    def create_time_tab(self):
        """ Create time tab with the possiblity of time range specification """

        self.timeTab = QtWidgets.QWidget()
        self.verticalLayoutTimeTab = QtWidgets.QVBoxLayout(self.timeTab)
        self.groupBoxStartTime = QtWidgets.QGroupBox(self.timeTab)
        self.horizontalLayoutStartTime = QtWidgets.QHBoxLayout(self.groupBoxStartTime)

        self.startDateEdit = QtWidgets.QDateEdit(self.groupBoxStartTime)
        self.startDateEdit.setDateTime(QDateTime.currentDateTime())
        self.startDateEdit.setMinimumSize(QtCore.QSize(200, 27))
        self.startDateEdit.setCalendarPopup(True)
        self.dateChange = True
        self.startDateEdit.dateChanged.connect(lambda x: self.enable_button('dateChange', self.startDateEdit.date() <= self.endDateEdit.date()))

        self.horizontalLayoutStartTime.addWidget(self.startDateEdit)

        # Default start Time Edit = 10 minutes ago
        minutes = 10

        self.startTimeEdit = QtWidgets.QTimeEdit(self.groupBoxStartTime)
        self.startTimeEdit.setTime(QTime.currentTime().addSecs(-minutes * 60))
        self.startTimeEdit.setMinimumSize(QtCore.QSize(80, 27))
        self.timeChange = True
        self.startTimeEdit.timeChanged.connect(lambda : self.enable_button('timeChange', self.startTimeEdit.time() <= self.endTimeEdit.time()))
        self.horizontalLayoutStartTime.addWidget(self.startTimeEdit)

        self.verticalLayoutTimeTab.addWidget(self.groupBoxStartTime)
        self.groupBoxEndTime = QtWidgets.QGroupBox(self.timeTab)
        self.horizontalLayoutEndTime = QtWidgets.QHBoxLayout(self.groupBoxEndTime)

        self.endDateEdit = QtWidgets.QDateEdit(self.groupBoxEndTime)
        self.endDateEdit.setDateTime(QDateTime.currentDateTime())
        self.endDateEdit.setMinimumSize(QtCore.QSize(200, 27))
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.dateChanged.connect(lambda x: self.enable_button('dateChange', self.startDateEdit.date() <= self.endDateEdit.date()))
        self.horizontalLayoutEndTime.addWidget(self.endDateEdit)

        self.endTimeEdit = QtWidgets.QTimeEdit(self.groupBoxEndTime)
        self.endTimeEdit.setTime(QTime.currentTime())
        self.endTimeEdit.setMinimumSize(QtCore.QSize(80, 27))
        self.endTimeEdit.timeChanged.connect(lambda : self.enable_button('timeChange', self.startTimeEdit.time() <= self.endTimeEdit.time()))
        self.horizontalLayoutEndTime.addWidget(self.endTimeEdit)

        self.verticalLayoutTimeTab.addWidget(self.groupBoxEndTime)
        self.tabWidget.addTab(self.timeTab, "")

    def retranslate_ui(self):
        """ Add all needed string labels to the Interface """

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Analyze Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.graphTab), _translate("MainWindow", "Graph parameters"))
        self.groupBoxSource.setTitle(_translate("MainWindow", "Source"))

        self.groupBoxHostDB.setTitle(_translate("MainWindow", "Hostname and Database"))
        self.groupBoxCredentials.setTitle(_translate("MainWindow", "Credentials"))
        self.groupBoxPortDB.setTitle(_translate("MainWindow", "Port number"))

        self.labelUsername.setText(_translate("MainWindow", "Username"))
        self.labelDatabase.setText(_translate("MainWindow", "Database"))
        self.labelHostname.setText(_translate("MainWindow", "Hostname"))
        self.labelPassword.setText(_translate("MainWindow", "Password"))
        self.labelDBPort.setText(_translate("MainWindow", "Port"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dbTab), _translate("MainWindow", "DB Connection"))


        self.labelSourceIPaddress.setText(_translate("MainWindow", "IP address"))
        self.labelSourcePort.setText(_translate("MainWindow", "Port"))
        self.groupBoxDestination.setTitle(_translate("MainWindow", "Destination"))
        self.labelDestinationIPaddress.setText(_translate("MainWindow", "IP address"))
        self.labelDestinationPort.setText(_translate("MainWindow", "Port"))
        self.groupBoxProtocol.setTitle(_translate("MainWindow", "Protocol"))
        self.labelProtocol.setText(_translate("MainWindow", "Protocol number"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.flowTab), _translate("MainWindow", "Flow parameters"))
        self.groupBoxStartTime.setTitle(_translate("MainWindow", "Select time of the first measurment"))
        self.groupBoxEndTime.setTitle(_translate("MainWindow", "Select time of last measurment"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timeTab), _translate("MainWindow", "Time"))

    def set_up_db_connection(self):
        self.dataProvider.set_up_connection(host=self.hostnameLineEdit.text(), user=self.usernameLineEdit.text(), \
        passwd=self.passwordLineEdit.text(), db=self.databaseLineEdit.text(), port=int(self.dbPortLineEdit.text()))

    def update(self):
        """ Get data from database with dataProvider and create graphs """

        self.set_up_db_connection()

        for ax in self.timeDeltaAxes:
            ax.clear()

        self.axOWD.clear()

        for tab in self.timedeltaTabs:
            index = self.plotTab.indexOf(tab)
            self.plotTab.removeTab(index)

        self.timeDeltaFigures = []
        self.amountOfTimedelta = 0
        self.timeDeltaAxes = []
        self.timedeltaTabs = []

        # Create query
        startTime = QDateTime(self.startDateEdit.date(), self.startTimeEdit.time()).toMSecsSinceEpoch() * 1000000
        endTime = QDateTime(self.endDateEdit.date(), self.endTimeEdit.time()).toMSecsSinceEpoch() * 1000000

        query = self.dataProvider.create_query(self.ipSrcLineEdit.text(),
                             self.maskSrcLineEdit.text(),
                             self.ipDstLineEdit.text(),
                             self.maskDstLineEdit.text(),
                             self.protocolLineEdit.text(),
                             self.portSrcLineEdit.text(),
                             self.portDstLineEdit.text(),
                             startTime,
                             endTime)

        if query is not None:
            dataFrame = self.dataProvider.get_data(query=query[0])
            dataFrameDelay = self.dataProvider.get_data(query=query[1])


            # Draw the graphs

            if dataFrame is not None and not dataFrame.empty:
                self.draw_timedelta_graph(dataFrame)

            if dataFrameDelay is not None and not dataFrameDelay.empty:

                # Check if the flow is unambiguous
                alert = 0
                warning = 0
                if self.maskSrcLineEdit.text() == '32' and self.maskDstLineEdit.text() == '32' and len(self.portSrcLineEdit.text()) > 0 and len(self.portDstLineEdit.text()) > 0 and len(self.protocolLineEdit.text()) > 0:
                   slaData = self.dataProvider.get_data(query=query[2])
                   if slaData is not None and not slaData.empty:
                       alert = slaData['delay_alert'].iloc[0]
                       warning = slaData['delay_warning'].iloc[0]

                self.draw_owd_graph(dataFrameDelay, alert, warning)


            self.owdFigure.autofmt_xdate(rotation=45)
            self.owdFigure.tight_layout(pad=4)
            #self.axOWD.yaxis.set_major_formatter( FormatStrFormatter("%1.2E ns"))
            self.axOWD.set_ylabel("ns")
            self.axOWD.xaxis.set_major_formatter( DateFormatter("%Y-%m-%d\n%H:%M:%S"))
            self.axOWD.xaxis_date()

            self.owdFigure.canvas.draw_idle()

            for ax in self.timeDeltaAxes:
        #        ax.yaxis.set_major_formatter( DateFormatter("%d us"))
                ax.xaxis.set_major_formatter( DateFormatter("%Y-%m-%d\n%H:%M:%S"))
                ax.xaxis_date()

            for figure in self.timeDeltaFigures:
                figure.autofmt_xdate(rotation=45)
                figure.tight_layout(pad=4)
                figure.canvas.draw_idle()




    def draw_timedelta_graph(self, df):

        groupedDataFrame = df.groupby('switch_ID')
        listOfDataFrames = [groupedDataFrame.get_group(g) for g in groupedDataFrame.groups]
        #print(listOfDataFrames)

        numberOfSwitches = len(listOfDataFrames)

        for switch in range(0, numberOfSwitches):
            df = listOfDataFrames[switch]
            self.add_timedelta_tab(df['switch_ID'].iloc[0])


            self.timeDeltaAxes[switch].plot_date(df['time'], df['avg_delta'], '-', color="#3F5D7D", lw=0.4)
            d = df['time'].values
            self.timeDeltaAxes[switch].fill_between(d, df['max_delta'], df['min_delta'], color="#aec7e8")


    def draw_owd_graph(self, df, alert, warning):

        self.axOWD.plot_date(df['time'], df['aver'], '-', color="#3F5D7D", lw=0.4)
        d = df['time'].values
        self.axOWD.fill_between(d, df['maxi'], df['mini'], color="#aec7e8")

        if warning > 0:
            self.axOWD.axhline(y=warning, linewidth=1, color='#800020')

        if alert > 0:
            self.axOWD.axhline(y=alert, linewidth=1, color='#800020')


class DataProvider:
    def __init__(self, host='localhost', port=3306, user='root', passwd='root',
                    db='testdb'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def set_up_connection(self, host='localhost', port=3306, user='root', passwd='root',
                    db='testdb'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def create_query(self, ipSrc, maskSrc, ipDst, maskDst, protocol, portSrc, portDst, timeBegin, timeEnd):
        """ Creates query with all needed parameters which will be then passed
        to the get_data function. """

        def group_sentence_timedelta(timeBegin, timeEnd, param):
            n = 5000 # liczba probek TODO: uzaleznic od przedzialu czasowego (?)
            timeslot = int((timeEnd - timeBegin)/n)
            group_clause = ' GROUP BY ROUND(%s/%d)' % (param, timeslot)
            return group_clause

        def group_sentence_timedelta_with_swid(timeBegin, timeEnd, param):
            n = 5000 # liczba probek TODO: uzaleznic od przedzialu czasowego (?)
            timeslot = int((timeEnd - timeBegin)/n)
            group_clause = ' GROUP BY switch_ID, ROUND(%s/%d)' % (param, timeslot)
            return group_clause

        def group_sentence():
            group_clause = ' GROUP BY Options.measurement_ID'
            return group_clause


        parameters = []
        join_string = "SELECT %s FROM Applications \
                       LEFT JOIN Measurments \
                       ON Applications.ID = Measurments.ID \
                       LEFT JOIN Options \
                       ON Options.measurement_ID = Measurments.measurement_ID"

        # Add IP_src and IP_dst query
        for ip, mask, parameter in zip((ipSrc, ipDst), (maskSrc, maskDst), ("IP_src", "IP_dst")):
            try:
                ip_lower, ip_upper, version = self.get_ip(ip, mask)
                parameters.append("%s >= %d AND %s <= %d" % (parameter, ip_lower, parameter, ip_upper))
            except ValueError:
                pass

        # Add swapped query
        try:
            swapped = 0 if int(portSrc) < int(portDst) else 1
            parameters.append("%s = %d" % ("swapped", swapped))
        except ValueError:
            pass

        # Add ports query
        for port, parameter in zip(sorted((portSrc, portDst), key=lambda x: x), ("port1", "port2")):
            try:
                parameters.append("%s = %d" %(parameter, int(port)))
            except ValueError:
                pass

        # Add protocol
        try:
            parameters.append("%s = %d" % ("protocol", int(protocol)))
        except ValueError:
            pass

        # Select time
        parameters.append("%s >= %d" % ("timestamp", timeBegin))
        parameters.append("%s <= %d" % ("timestamp", timeEnd))

        # Select parameters to query TODO!
        # For timedelta
        queriedParameteres = ",".join(("seq_nr", "FROM_UNIXTIME(timestamp/1000000000) as time", "MAX(timedelta) as max_delta", "AVG(timedelta) as avg_delta", "MIN(timedelta) as min_delta", "switch_ID"))
        # Other
        queriedParameteres2 = ",".join(("seq_nr","MAX(timestamp) - MIN(timestamp) as timestamp_delta", "FROM_UNIXTIME(MAX(timestamp)/1000000000) as time", "MAX(timestamp) as max"))

        flow = ipDst + "." + ipSrc + "." + str(portDst) + "." + str(portSrc) + "." + str(protocol)

        if len(parameters) > 0:
            return [(join_string % (queriedParameteres)) + " WHERE " + " AND ".join(parameters) + group_sentence_timedelta_with_swid(timeBegin, timeEnd, "timestamp"),
                    "SELECT MAX(timestamp_delta) as maxi, MIN(timestamp_delta) as mini, AVG(timestamp_delta) as aver, time, max FROM (" + (join_string % (queriedParameteres2)) + " WHERE " + " AND ".join(parameters) + group_sentence() + ") AS temp " + group_sentence_timedelta(timeBegin, timeEnd, "max"),
                    "SELECT delay_warning, delay_alert FROM SLA WHERE flow = \'" + flow + "\'"]
        else:
            return None


    def get_ip(self, ip, mask):
        import socket
        import binascii

        """
        Converts an IP address (expressed as a string e.g. "10.0.3.10")
        with mask (expressed as an integer e.g. "24")
        to its integer representation range (returns tuple -  first ip
        address, second ip address and protocol version).
        The function tries first to parse the IP as IPv4, then as IPv6.
        """
        try:
            network_prefix = ip
            netmask_len = int(mask)

            for version in (socket.AF_INET, socket.AF_INET6):

                ip_len = 32 if version == socket.AF_INET else 128

                try:
                    suffix_mask = (1 << (ip_len - netmask_len)) - 1
                    netmask = ((1 << ip_len) - 1) - suffix_mask
                    ip_hex = socket.inet_pton(version, network_prefix)
                    ip_lower = int(binascii.hexlify(ip_hex), 16) & netmask
                    ip_upper = ip_lower + suffix_mask

                    return (ip_lower,
                            ip_upper,
                            4 if version == socket.AF_INET else 6)
                except:
                    pass
        except:
            pass

        raise ValueError # TODO: poprawna obsluga bledow


    def get_data(self, query=''):
        try:
            mysql_cn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db)
            df_mysql = pd.read_sql(query, con=mysql_cn)
            mysql_cn.close()

            return df_mysql

        except (MySQLdb.Error, MySQLdb.Warning, pd.io.sql.DatabaseError) as e:
            print(e)    # TODO: change to logging to file
            return None


if __name__ == '__main__':


    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainWindow()
    sys.exit(app.exec_())
