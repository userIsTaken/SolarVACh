# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(528, 550)
        self.gridLayout = QtWidgets.QGridLayout(SettingsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_3 = QtWidgets.QFrame(SettingsDialog)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.fb_scan = QtWidgets.QCheckBox(self.frame_3)
        self.fb_scan.setMaximumSize(QtCore.QSize(16777215, 24))
        self.fb_scan.setObjectName("fb_scan")
        self.gridLayout_5.addWidget(self.fb_scan, 4, 0, 1, 1)
        self.sc_name = QtWidgets.QTextEdit(self.frame_3)
        self.sc_name.setMaximumSize(QtCore.QSize(16777215, 25))
        self.sc_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sc_name.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sc_name.setObjectName("sc_name")
        self.gridLayout_5.addWidget(self.sc_name, 2, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 1, 1, 1)
        self.frame_4 = QtWidgets.QFrame(SettingsDialog)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.frame_4)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_4)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setWordWrap(False)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 1, 1, 1)
        self.array_size_box = QtWidgets.QSpinBox(self.frame_4)
        self.array_size_box.setMaximum(10000)
        self.array_size_box.setObjectName("array_size_box")
        self.gridLayout_3.addWidget(self.array_size_box, 2, 0, 1, 1)
        self.x_mean_box = QtWidgets.QDoubleSpinBox(self.frame_4)
        self.x_mean_box.setDecimals(3)
        self.x_mean_box.setObjectName("x_mean_box")
        self.gridLayout_3.addWidget(self.x_mean_box, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_4)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 0, 1, 1)
        self.wait_box = QtWidgets.QSpinBox(self.frame_4)
        self.wait_box.setMaximum(1000)
        self.wait_box.setObjectName("wait_box")
        self.gridLayout_3.addWidget(self.wait_box, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(SettingsDialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)
        self.startV_box = QtWidgets.QDoubleSpinBox(self.frame)
        self.startV_box.setMinimum(-20.0)
        self.startV_box.setMaximum(20.0)
        self.startV_box.setObjectName("startV_box")
        self.gridLayout_2.addWidget(self.startV_box, 2, 0, 1, 1)
        self.limitA_box = QtWidgets.QDoubleSpinBox(self.frame)
        self.limitA_box.setObjectName("limitA_box")
        self.gridLayout_2.addWidget(self.limitA_box, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 1, 1, 1)
        self.endV_box = QtWidgets.QDoubleSpinBox(self.frame)
        self.endV_box.setMinimum(-20.0)
        self.endV_box.setMaximum(20.0)
        self.endV_box.setObjectName("endV_box")
        self.gridLayout_2.addWidget(self.endV_box, 4, 0, 1, 1)
        self.points_box = QtWidgets.QSpinBox(self.frame)
        self.points_box.setMaximum(10000)
        self.points_box.setObjectName("points_box")
        self.gridLayout_2.addWidget(self.points_box, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.frame_2 = QtWidgets.QFrame(SettingsDialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_18 = QtWidgets.QLabel(self.frame_2)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_4.addWidget(self.label_18, 0, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.frame_2)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setWordWrap(False)
        self.label_20.setObjectName("label_20")
        self.gridLayout_4.addWidget(self.label_20, 0, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.frame_2)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 2, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.frame_2)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setWordWrap(False)
        self.label_21.setObjectName("label_21")
        self.gridLayout_4.addWidget(self.label_21, 2, 1, 1, 1)
        self.electrode_combo = QtWidgets.QComboBox(self.frame_2)
        self.electrode_combo.setObjectName("electrode_combo")
        self.electrode_combo.addItem("")
        self.electrode_combo.addItem("")
        self.electrode_combo.addItem("")
        self.electrode_combo.addItem("")
        self.electrode_combo.addItem("")
        self.electrode_combo.addItem("")
        self.gridLayout_4.addWidget(self.electrode_combo, 3, 0, 1, 1)
        self.relay_combo = QtWidgets.QComboBox(self.frame_2)
        self.relay_combo.setObjectName("relay_combo")
        self.relay_combo.addItem("")
        self.relay_combo.addItem("")
        self.relay_combo.addItem("")
        self.relay_combo.addItem("")
        self.relay_combo.addItem("")
        self.relay_combo.addItem("")
        self.gridLayout_4.addWidget(self.relay_combo, 3, 1, 1, 1)
        self.power_input_box = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.power_input_box.setMaximum(1000.0)
        self.power_input_box.setObjectName("power_input_box")
        self.gridLayout_4.addWidget(self.power_input_box, 1, 1, 1, 1)
        self.area_box = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.area_box.setObjectName("area_box")
        self.gridLayout_4.addWidget(self.area_box, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.fb_scan.setText(_translate("SettingsDialog", "Forward-Backward Scan"))
        self.label_16.setText(_translate("SettingsDialog", "SC name:"))
        self.label_6.setText(_translate("SettingsDialog", "Error"))
        self.label_7.setText(_translate("SettingsDialog", "Size of array"))
        self.label_9.setText(_translate("SettingsDialog", "<html><head/><body><p>x<span style=\" vertical-align:sub;\">mean</span>/𝚫x</p></body></html>"))
        self.label_8.setText(_translate("SettingsDialog", "Wait[ms]"))
        self.label.setText(_translate("SettingsDialog", "Voltage"))
        self.label_2.setText(_translate("SettingsDialog", "Start [V]"))
        self.label_4.setText(_translate("SettingsDialog", "Current limit [A]"))
        self.label_3.setText(_translate("SettingsDialog", "End [V]"))
        self.label_5.setText(_translate("SettingsDialog", "Points"))
        self.label_18.setText(_translate("SettingsDialog", "<html><head/><body><p>Area of <br/>electrode [mm<span style=\" vertical-align:super;\">2</span>]</p></body></html>"))
        self.label_20.setText(_translate("SettingsDialog", "<html><head/><body><p>Power input<br/>[mW/cm<span style=\" vertical-align:super;\">2</span>]</p></body></html>"))
        self.label_19.setText(_translate("SettingsDialog", "<html><head/><body><p>Number of <br/>electrodes</p></body></html>"))
        self.label_21.setText(_translate("SettingsDialog", "<html><head/><body><p>Start from <br/>relay:</p></body></html>"))
        self.electrode_combo.setItemText(0, _translate("SettingsDialog", "1"))
        self.electrode_combo.setItemText(1, _translate("SettingsDialog", "2"))
        self.electrode_combo.setItemText(2, _translate("SettingsDialog", "3"))
        self.electrode_combo.setItemText(3, _translate("SettingsDialog", "4"))
        self.electrode_combo.setItemText(4, _translate("SettingsDialog", "5"))
        self.electrode_combo.setItemText(5, _translate("SettingsDialog", "6"))
        self.relay_combo.setItemText(0, _translate("SettingsDialog", "1"))
        self.relay_combo.setItemText(1, _translate("SettingsDialog", "2"))
        self.relay_combo.setItemText(2, _translate("SettingsDialog", "3"))
        self.relay_combo.setItemText(3, _translate("SettingsDialog", "4"))
        self.relay_combo.setItemText(4, _translate("SettingsDialog", "5"))
        self.relay_combo.setItemText(5, _translate("SettingsDialog", "6"))

