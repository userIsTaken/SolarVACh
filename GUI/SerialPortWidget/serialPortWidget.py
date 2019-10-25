from GUI.SerialPortWidget.SerialPortUI import Ui_serialPortWidget
import sys, os
from PyQt5 import QtWidgets

class serialPortWidget(QtWidgets.QWidget):
    def __init__(self):
        super(serialPortWidget, self).__init__()
        self.ui = Ui_serialPortWidget()
        pass