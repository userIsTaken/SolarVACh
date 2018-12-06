# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Solar.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(742, 731)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(120, 80))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 71, 61))
        self.pushButton.setObjectName("pushButton")
        self.device_box = QtWidgets.QComboBox(self.frame)
        self.device_box.setGeometry(QtCore.QRect(100, 40, 101, 21))
        self.device_box.setObjectName("device_box")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(120, 20, 54, 17))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setGeometry(QtCore.QRect(83, 10, 20, 61))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.channel_box = QtWidgets.QComboBox(self.frame)
        self.channel_box.setGeometry(QtCore.QRect(220, 40, 101, 21))
        self.channel_box.setObjectName("channel_box")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(240, 20, 54, 17))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_16 = QtWidgets.QLabel(self.frame)
        self.label_16.setGeometry(QtCore.QRect(400, 20, 101, 17))
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.save_slot = QtWidgets.QTextEdit(self.frame)
        self.save_slot.setGeometry(QtCore.QRect(340, 40, 221, 21))
        self.save_slot.setObjectName("save_slot")
        self.label_17 = QtWidgets.QLabel(self.frame)
        self.label_17.setGeometry(QtCore.QRect(595, 20, 101, 17))
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.save_slot_2 = QtWidgets.QTextEdit(self.frame)
        self.save_slot_2.setGeometry(QtCore.QRect(580, 40, 131, 21))
        self.save_slot_2.setObjectName("save_slot_2")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.vach_tab = QtWidgets.QWidget()
        self.vach_tab.setObjectName("vach_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.vach_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.power_graph = PlotWidget(self.vach_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_graph.sizePolicy().hasHeightForWidth())
        self.power_graph.setSizePolicy(sizePolicy)
        self.power_graph.setMinimumSize(QtCore.QSize(300, 200))
        self.power_graph.setObjectName("power_graph")
        self.gridLayout_2.addWidget(self.power_graph, 1, 2, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.vach_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(700, 300))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 300))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(330, 144))
        self.frame_3.setMaximumSize(QtCore.QSize(330, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_8.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_8.addWidget(self.label_4, 1, 1, 1, 1)
        self.startV_box = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.startV_box.setObjectName("startV_box")
        self.gridLayout_8.addWidget(self.startV_box, 2, 0, 1, 1)
        self.limitA_box = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.limitA_box.setObjectName("limitA_box")
        self.gridLayout_8.addWidget(self.limitA_box, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_8.addWidget(self.label_5, 3, 1, 1, 1)
        self.endV_box = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.endV_box.setObjectName("endV_box")
        self.gridLayout_8.addWidget(self.endV_box, 4, 0, 1, 1)
        self.points_box = QtWidgets.QSpinBox(self.frame_3)
        self.points_box.setObjectName("points_box")
        self.gridLayout_8.addWidget(self.points_box, 4, 1, 1, 1)
        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 1, 1)
        self.current_graph = PlotWidget(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.current_graph.sizePolicy().hasHeightForWidth())
        self.current_graph.setSizePolicy(sizePolicy)
        self.current_graph.setMinimumSize(QtCore.QSize(200, 150))
        self.current_graph.setMaximumSize(QtCore.QSize(330, 300))
        self.current_graph.setSizeIncrement(QtCore.QSize(0, 0))
        self.current_graph.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.current_graph.setObjectName("current_graph")
        self.gridLayout_3.addWidget(self.current_graph, 0, 1, 2, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setMinimumSize(QtCore.QSize(330, 135))
        self.frame_4.setMaximumSize(QtCore.QSize(330, 135))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_7 = QtWidgets.QLabel(self.frame_4)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_7.addWidget(self.label_7, 0, 0, 1, 1)
        self.array_size_box = QtWidgets.QSpinBox(self.frame_4)
        self.array_size_box.setObjectName("array_size_box")
        self.gridLayout_7.addWidget(self.array_size_box, 1, 0, 1, 1)
        self.wait_box = QtWidgets.QSpinBox(self.frame_4)
        self.wait_box.setObjectName("wait_box")
        self.gridLayout_7.addWidget(self.wait_box, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_4)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_7.addWidget(self.label_8, 2, 0, 1, 1)
        self.x_mean_box = QtWidgets.QDoubleSpinBox(self.frame_4)
        self.x_mean_box.setObjectName("x_mean_box")
        self.gridLayout_7.addWidget(self.x_mean_box, 3, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_4)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setWordWrap(False)
        self.label_9.setObjectName("label_9")
        self.gridLayout_7.addWidget(self.label_9, 2, 2, 1, 1)
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
        self.gridLayout_7.addWidget(self.label_6, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.frame_4, 1, 0, 2, 1)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QtCore.QSize(330, 120))
        self.frame_6.setMaximumSize(QtCore.QSize(330, 120))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.label_18 = QtWidgets.QLabel(self.frame_6)
        self.label_18.setGeometry(QtCore.QRect(10, 30, 141, 17))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.label_20 = QtWidgets.QLabel(self.frame_6)
        self.label_20.setGeometry(QtCore.QRect(170, 30, 141, 17))
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setWordWrap(False)
        self.label_20.setObjectName("label_20")
        self.area_box = QtWidgets.QSpinBox(self.frame_6)
        self.area_box.setGeometry(QtCore.QRect(30, 55, 91, 27))
        self.area_box.setObjectName("area_box")
        self.power_input_box = QtWidgets.QSpinBox(self.frame_6)
        self.power_input_box.setGeometry(QtCore.QRect(190, 55, 91, 27))
        self.power_input_box.setObjectName("power_input_box")
        self.gridLayout_3.addWidget(self.frame_6, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 2, 2, 1, 1)
        self.current_graph.raise_()
        self.frame_3.raise_()
        self.frame_6.raise_()
        self.frame_4.raise_()
        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 3)
        self.frame_5 = QtWidgets.QFrame(self.vach_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setMinimumSize(QtCore.QSize(90, 200))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_12 = QtWidgets.QLabel(self.frame_5)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.lcdNumber = QtWidgets.QLCDNumber(self.frame_5)
        self.lcdNumber.setObjectName("lcdNumber")
        self.verticalLayout.addWidget(self.lcdNumber)
        self.label_13 = QtWidgets.QLabel(self.frame_5)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.frame_5)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.verticalLayout.addWidget(self.lcdNumber_2)
        self.label_14 = QtWidgets.QLabel(self.frame_5)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout.addWidget(self.label_14)
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.frame_5)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.verticalLayout.addWidget(self.lcdNumber_3)
        self.label_15 = QtWidgets.QLabel(self.frame_5)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout.addWidget(self.label_15)
        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.frame_5)
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.verticalLayout.addWidget(self.lcdNumber_4)
        self.gridLayout_2.addWidget(self.frame_5, 1, 1, 1, 1)
        self.density_graph = PlotWidget(self.vach_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.density_graph.sizePolicy().hasHeightForWidth())
        self.density_graph.setSizePolicy(sizePolicy)
        self.density_graph.setMinimumSize(QtCore.QSize(300, 200))
        self.density_graph.setObjectName("density_graph")
        self.gridLayout_2.addWidget(self.density_graph, 1, 0, 1, 1)
        self.tabWidget.addTab(self.vach_tab, "")
        self.time_tab = QtWidgets.QWidget()
        self.time_tab.setObjectName("time_tab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.time_tab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.graphicsView = PlotWidget(self.time_tab)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_6.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.graphicsView_2 = PlotWidget(self.time_tab)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.gridLayout_6.addWidget(self.graphicsView_2, 0, 1, 1, 1)
        self.graphicsView_3 = PlotWidget(self.time_tab)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.gridLayout_6.addWidget(self.graphicsView_3, 1, 0, 1, 1)
        self.graphicsView_4 = PlotWidget(self.time_tab)
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.gridLayout_6.addWidget(self.graphicsView_4, 1, 1, 1, 1)
        self.graphicsView_5 = PlotWidget(self.time_tab)
        self.graphicsView_5.setObjectName("graphicsView_5")
        self.gridLayout_6.addWidget(self.graphicsView_5, 2, 0, 1, 1)
        self.graphicsView_6 = PlotWidget(self.time_tab)
        self.graphicsView_6.setObjectName("graphicsView_6")
        self.gridLayout_6.addWidget(self.graphicsView_6, 2, 1, 1, 1)
        self.tabWidget.addTab(self.time_tab, "")
        self.opt_tab = QtWidgets.QWidget()
        self.opt_tab.setObjectName("opt_tab")
        self.formLayout = QtWidgets.QFormLayout(self.opt_tab)
        self.formLayout.setObjectName("formLayout")
        self.widget = QtWidgets.QWidget(self.opt_tab)
        self.widget.setMaximumSize(QtCore.QSize(300, 160))
        self.widget.setObjectName("widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.electrode_combo = QtWidgets.QComboBox(self.widget)
        self.electrode_combo.setObjectName("electrode_combo")
        self.gridLayout_4.addWidget(self.electrode_combo, 0, 1, 1, 1)
        self.relay_combo = QtWidgets.QComboBox(self.widget)
        self.relay_combo.setObjectName("relay_combo")
        self.gridLayout_4.addWidget(self.relay_combo, 1, 1, 1, 1)
        self.fb_scan = QtWidgets.QCheckBox(self.widget)
        self.fb_scan.setMaximumSize(QtCore.QSize(16777215, 24))
        self.fb_scan.setObjectName("fb_scan")
        self.gridLayout_4.addWidget(self.fb_scan, 2, 0, 1, 2)
        self.label_19 = QtWidgets.QLabel(self.widget)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout_4.addWidget(self.label_19, 0, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.widget)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setWordWrap(False)
        self.label_21.setObjectName("label_21")
        self.gridLayout_4.addWidget(self.label_21, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 1, 1, 1)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widget)
        self.frame_7 = QtWidgets.QFrame(self.opt_tab)
        self.frame_7.setMaximumSize(QtCore.QSize(350, 125))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.ip_address = QtWidgets.QTextEdit(self.frame_7)
        self.ip_address.setMaximumSize(QtCore.QSize(256, 41))
        self.ip_address.setObjectName("ip_address")
        self.gridLayout_9.addWidget(self.ip_address, 2, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.frame_7)
        self.label_23.setObjectName("label_23")
        self.gridLayout_9.addWidget(self.label_23, 2, 0, 1, 1)
        self.connect_button = QtWidgets.QPushButton(self.frame_7)
        self.connect_button.setObjectName("connect_button")
        self.gridLayout_9.addWidget(self.connect_button, 3, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setTextFormat(QtCore.Qt.PlainText)
        self.label_22.setObjectName("label_22")
        self.gridLayout_9.addWidget(self.label_22, 1, 1, 1, 1)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.frame_7)
        self.tabWidget.addTab(self.opt_tab, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 742, 32))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.label_10.setText(_translate("MainWindow", "Device"))
        self.label_11.setText(_translate("MainWindow", "Channel"))
        self.label_16.setText(_translate("MainWindow", "Save directory:"))
        self.label_17.setText(_translate("MainWindow", "SC name:"))
        self.label.setText(_translate("MainWindow", "Voltage"))
        self.label_2.setText(_translate("MainWindow", "Start [V]"))
        self.label_4.setText(_translate("MainWindow", "Current limit [A]"))
        self.label_3.setText(_translate("MainWindow", "End [V]"))
        self.label_5.setText(_translate("MainWindow", "Points"))
        self.label_7.setText(_translate("MainWindow", "Size of array"))
        self.label_8.setText(_translate("MainWindow", "Wait[ms]"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p>x<span style=\" vertical-align:sub;\">mean</span>/𝚫x</p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "Error"))
        self.label_18.setText(_translate("MainWindow", "<html><head/><body><p>Area of electrode [mm<span style=\" vertical-align:super;\">2</span>]</p></body></html>"))
        self.label_20.setText(_translate("MainWindow", "<html><head/><body><p>Power input[mW/cm<span style=\" vertical-align:super;\">2</span>]</p></body></html>"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">𝜂, %</span></p></body></html>"))
        self.label_13.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">FF, %</span></p></body></html>"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">U</span><span style=\" font-weight:600; vertical-align:sub;\">oc</span><span style=\" font-weight:600;\">, V</span></p></body></html>"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">J</span><span style=\" font-weight:600; vertical-align:sub;\">sc</span><span style=\" font-weight:600;\">, mA/cm</span><span style=\" font-weight:600; vertical-align:super;\">2</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.vach_tab), _translate("MainWindow", "VACh"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.time_tab), _translate("MainWindow", "Time functions"))
        self.fb_scan.setText(_translate("MainWindow", "Forward-Backward Scan"))
        self.label_19.setText(_translate("MainWindow", "<html><head/><body><p>Number of electrodes:</p></body></html>"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p>Start from relay:</p></body></html>"))
        self.label_23.setText(_translate("MainWindow", "Device IP :"))
        self.connect_button.setText(_translate("MainWindow", "Connect"))
        self.label_22.setText(_translate("MainWindow", "DEVICE CONFIGURATION"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.opt_tab), _translate("MainWindow", "Options"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit(Ctrl+Q)"))

from pyqtgraph import PlotWidget
