# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serialPortWidgetForm.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_serialPortWidget(object):
    def setupUi(self, serialPortWidget):
        serialPortWidget.setObjectName("serialPortWidget")
        serialPortWidget.resize(358, 197)
        self.gridLayout = QtWidgets.QGridLayout(serialPortWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.labelCOM = QtWidgets.QLabel(serialPortWidget)
        self.labelCOM.setObjectName("labelCOM")
        self.gridLayout.addWidget(self.labelCOM, 0, 0, 1, 1)
        self.comPortBox = QtWidgets.QComboBox(serialPortWidget)
        self.comPortBox.setObjectName("comPortBox")
        self.gridLayout.addWidget(self.comPortBox, 0, 2, 1, 1)
        self.labelBaud = QtWidgets.QLabel(serialPortWidget)
        self.labelBaud.setObjectName("labelBaud")
        self.gridLayout.addWidget(self.labelBaud, 1, 0, 1, 1)
        self.baudRateBox = QtWidgets.QComboBox(serialPortWidget)
        self.baudRateBox.setObjectName("baudRateBox")
        self.gridLayout.addWidget(self.baudRateBox, 1, 2, 1, 1)
        self.labelData = QtWidgets.QLabel(serialPortWidget)
        self.labelData.setObjectName("labelData")
        self.gridLayout.addWidget(self.labelData, 2, 0, 1, 1)
        self.dataBitsInformation = QtWidgets.QLabel(serialPortWidget)
        self.dataBitsInformation.setObjectName("dataBitsInformation")
        self.gridLayout.addWidget(self.dataBitsInformation, 2, 1, 1, 1)
        self.dataBitsBox = QtWidgets.QComboBox(serialPortWidget)
        self.dataBitsBox.setObjectName("dataBitsBox")
        self.gridLayout.addWidget(self.dataBitsBox, 2, 2, 1, 1)
        self.labelStop = QtWidgets.QLabel(serialPortWidget)
        self.labelStop.setObjectName("labelStop")
        self.gridLayout.addWidget(self.labelStop, 3, 0, 1, 1)
        self.StopBitsInformation = QtWidgets.QLabel(serialPortWidget)
        self.StopBitsInformation.setObjectName("StopBitsInformation")
        self.gridLayout.addWidget(self.StopBitsInformation, 3, 1, 1, 1)
        self.stopBitsBox = QtWidgets.QComboBox(serialPortWidget)
        self.stopBitsBox.setObjectName("stopBitsBox")
        self.gridLayout.addWidget(self.stopBitsBox, 3, 2, 1, 1)
        self.labelParity = QtWidgets.QLabel(serialPortWidget)
        self.labelParity.setObjectName("labelParity")
        self.gridLayout.addWidget(self.labelParity, 4, 0, 1, 1)
        self.parityInformation = QtWidgets.QLabel(serialPortWidget)
        self.parityInformation.setObjectName("parityInformation")
        self.gridLayout.addWidget(self.parityInformation, 4, 1, 1, 1)
        self.parityBox = QtWidgets.QComboBox(serialPortWidget)
        self.parityBox.setObjectName("parityBox")
        self.gridLayout.addWidget(self.parityBox, 4, 2, 1, 1)

        self.retranslateUi(serialPortWidget)
        QtCore.QMetaObject.connectSlotsByName(serialPortWidget)

    def retranslateUi(self, serialPortWidget):
        _translate = QtCore.QCoreApplication.translate
        serialPortWidget.setWindowTitle(_translate("serialPortWidget", "Form"))
        self.labelCOM.setText(_translate("serialPortWidget", "COM port"))
        self.labelBaud.setText(_translate("serialPortWidget", "Baud Rate"))
        self.labelData.setText(_translate("serialPortWidget", "Data Bits"))
        self.dataBitsInformation.setText(_translate("serialPortWidget", "?"))
        self.labelStop.setText(_translate("serialPortWidget", "Stop Bits"))
        self.StopBitsInformation.setText(_translate("serialPortWidget", "?"))
        self.labelParity.setText(_translate("serialPortWidget", "Parity"))
        self.parityInformation.setText(_translate("serialPortWidget", "?"))

