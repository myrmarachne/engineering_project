import logging
import sys
import netifaces
import os
import re
from PyQt5 import QtWidgets, QtCore

import qdarkstyle
import ui.ui as ui_module

def main():

    logging.basicConfig(level=logging.DEBUG)

    scriptPath = sys.argv[0]
    filename = os.path.basename(scriptPath)
    directory = re.sub(filename+'$', '', scriptPath)

    os.chdir(directory)
    os.chdir("../") # Changing directory to the sniffer_module

    configPath = os.path.join(os.getcwd(), "backend", "conf", "conf.json")

    jsonHandler = ui_module.JsonHandler(configPath)

    app = QtWidgets.QApplication(sys.argv)  # Create the application and the main window
    window = QtWidgets.QMainWindow()

    # Setup User Interface
    ui = ui_module.Ui_MainWindow()
    ui.setupUi(window)
    ui.addJsonHandler(jsonHandler)

    ui.addCallbacks(window)

    interfaces = netifaces.interfaces()
    ui.addInterfaces(interfaces)

    window.setWindowTitle("Set up connection")

    # Setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # Run
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
