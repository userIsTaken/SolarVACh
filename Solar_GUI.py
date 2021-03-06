from PyQt5 import QtWidgets, QtGui, QtCore
from GUI.Solar import Ui_MainWindow
from PopUp import PopUp
from HardwareAccess.KeysightWrapper import SourceMeter
from HardwareAccess.Keysight_USB import SourceMeter_USB
from ExpLoops.ExpLoop import *
from ExpLoops.CObservation import *
from ExpLoops.RelayObservation import *
from ExpLoops.RelayCO import *
from pyqtgraph import mkPen
import pyqtgraph as pg
from Config.confparser import *
import datetime
from random import randint
from HardwareAccess.KeithleyWrapper import SourceMeter_KTHL
from HardwareAccess.MotorWrapper import Motor
import traceback

from vars import *


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ThreadPool = QThreadPool()
        # self._threads = []
        self._thread = None
        self._worker = None
        self._threads = []
        # self._threads.append((self._thread, self._worker))
        self._path = None
        self.ExpensiveMeter = None
        self.ip = None
        self._usb = None
        self.jvView = self.ui.density_graph
        self.parameters = {} # global dictionary
        self.current_arr = []
        self.voltage_arr = []
    #     for analysis
        self.curr_array_analysis= []
        self.voltage_array_analysis = []
        # for observations over time:
        self.t_time_bw = []
        self.t_time_fw = []
        self.ff_time = []
        self.jsc_time = []
        self.Uoc_time = []
        self.PCE_time = []
        # for relay-based time observations:
        self._time_c = [[],[],[],[],[],[]]
        # no more than 6 relays:
        self._pce_c = [[],[],[],[],[],[]]
        self._ff_c = [[],[],[],[],[],[]]
        self._jsc_c= [[],[],[],[],[],[]]
        self._uoc_c= [[],[],[],[],[],[]]
        # Colors:
        self.RED = (255,0,0)
        self.CUSTOM=(255, 255, 102)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.SKYBLUE= (0,191,255)
        self.YELLOW = (215,215,0)
        self.VIOLET = (255, 0, 255)
        self.WHITE = (255,255,255)
        self.color = {1: self.RED,
                      2: self.GREEN,
                      3: self.BLUE,
                      4: self.WHITE,
                      5: self.YELLOW,
                      6: self.VIOLET}
        self.max_array = 45
        self.setupUI()
        self.motor = None
        self._params_updated = False
        self._line_ending_usb = None
        self.populate_usbtmc()
        self._demo_ = False
        self._t1 = None
        self._t2 = None
        self._t_diff = None
        self.__connect_listeners()
        pass

    def text_changed(self):
        self._params_updated = True
        pass

    def __connect_listeners(self):
        self.ui.connect_button.clicked.connect(self.MeterConnect)
        self.ui.startButton.clicked.connect(self.hell)
        self.ui.quitButton.clicked.connect(self.quit)
        self.ui.fullscreenButton.clicked.connect(self.fullscreen)
        self.ui.stopButton.clicked.connect(self.stopExperiment)
        self.ui.actionQuit.triggered.connect(self.quit)
        self.ui.actionDemo_mode.triggered.connect(self.debug)

        # save button
        self.ui.save_as_button.clicked.connect(self.save_results)
        self.ui.directory_button.clicked.connect(self.select_path)
        #     Shortcuts:
        self.quit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
        # events of shortcuts:
        self.quit_shortcut.activated.connect(self.quit)
        #     relay combos:
        #     self.ui.relay_combo.currentIndexChanged.connect(self.updateCombos)
        self.ui.device_box.currentIndexChanged.connect(self.updateDevices)
        # control of a motor:
        self.ui.motorButton.clicked.connect(self.motorFn)
        self.ui.turnCWbutton.clicked.connect(self.CW)
        self.ui.turnCCWbutton.clicked.connect(self.CCW)
        # degree entry control:
        self.ui.degreeBox.valueChanged.connect(self.setStepsFromDegrees)
        self.ui.connectUSBbutton.clicked.connect(self.usbtmc_connect)
        self.ui.rescanButton.clicked.connect(self.populate_usbtmc)
        self.ui.params_field.textChanged.connect(self.text_changed)
        pass


    def debug(self):
        if not self._demo_:
            self.ui.startButton.setEnabled(True)
            self._demo_ = True
            self.ui.statusbar.showMessage("DEMO. Not connected to any device!")
        elif self._demo_:
            self._demo_ = False
        pass

    def populate_usbtmc(self):
        try:
            self.ui.usbtmcComboBox.clear()
            mypath = "/dev"
            for f in os.listdir(mypath):
                if f.startswith('usbtmc'):
                    self.ui.usbtmcComboBox.addItem(mypath + "/" + f)
            indexes = self.ui.usbtmcComboBox.count()
            console("Indexes were :", str(indexes))
            if indexes == 0:
                self.ui.connectUSBbutton.setEnabled(False)
        except Exception as ex:
            console(str(ex))
        pass

    def usbtmc_connect(self):
        self._usb = self.ui.usbtmcComboBox.currentText()
        self._line_ending_usb = self.ui.lineEndingBox.currentText()
        e = None
        if "win" in self._line_ending_usb.lower():
            e = "\r\n"
        elif "lin" in self._line_ending_usb.lower():
            e = "\n"
        elif "mac" in self._line_ending_usb.lower():
            e = "\r"
        else:
            e = "\r\n"
        try:
            if self.ui.device_box.currentText().lower() in 'keysight':
                self.ExpensiveMeter = SourceMeter_USB(self._usb, e)
                id = self.ExpensiveMeter.ID
                self.ui.connectionErrorsBox.setPlainText(
                    "Connected successfully @" + str(self._usb) + "\nIDN:" + self.ExpensiveMeter.ID)
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.startButton.setEnabled(True)
                self.updateDevices()
                # update defaults:
                write_path_line(self._usb, e)
            else:
                pass
        except Exception as ex:
            console("ERROR in usb connection")
            console(str(ex))
            pass

    def setStepsFromDegrees(self):
        y = self.ui.degreeBox.value()
        x = (512.0*y)/360.0
        self.ui.stepsBox.setValue(int(x))
        pass

    def CW(self):
        steps = self.ui.stepsBox.value()
        result = self.motor.move_motor_cw(steps)
        self.ui.infoBox.setText(str(result)+" CW result")
        self.motor.low_pins()
        pass

    def CCW(self):
        steps = self.ui.stepsBox.value()
        result = self.motor.move_motor_ccw(steps)
        self.ui.infoBox.setText(str(result)+" CCW result")
        self.motor.low_pins()
        pass

    def motorFn(self):
        if "Connect to" in self.ui.motorButton.text():
            self.motor = Motor()
            IP = getGPIOip()
            self.motor.set_ip(IP)
            console(IP, ' motor IP')
            self.motor.setup()
            self.ui.infoBox.setText(str(self.motor.Local))
            self.ui.motorButton.setText("Disconnect from motor")
            pass
        elif "Disconnect from" in self.ui.motorButton.text():
            self.motor.low_pins()
            self.motor = None
            self.ui.motorButton.setText("Connect to motor")


    def updateDevices(self):
        if self.ui.device_box.currentIndex() == 0:
            self.ui.channel_box.setEnabled(True)
            self.max_array = 60
            self.ui.array_size_box.setMaximum(self.max_array)
        if self.ui.device_box.currentIndex() == 1:
            self.ui.channel_box.setEnabled(False)
            self.max_array = 1000
            self.ui.array_size_box.setMaximum(self.max_array)
        console(self.max_array, " : MAX ARRAY")
        if (self.ui.device_box.currentText().lower() in "keysight"):
            self.ui.connectUSBbutton.setEnabled(True)
        else:
            self.ui.connectUSBbutton.setEnabled(False)
        indexes = self.ui.usbtmcComboBox.count()
        if indexes == 0:
            self.ui.connectUSBbutton.setEnabled(False)

    def setupUI(self):
        self.ui.params_field.setPlainText(
            'SC ; F/B ; Uoc ; jsc ; FF ; Umax ; jmax ; Pmax ; PCE; S; t')
        self.ui.params_field.append(" [?] ; [?] ; [V] ; [mA/cm^2] ; [%] ; [V] ; [mA/cm^2] ; [mW/cm^2] ; [%] ; [cm^2]; [min.]")
        path, ip = get_path_ip()
        if ip is not None:
            self.ui.ip_address.setPlainText(ip)
        if path is not None:
            self.ui.directory_path.setPlainText(path)
        # file names:
        now = datetime.datetime.now()
        st = now.strftime('%Y_%m_%d_%Hval%Mmin')
        self.ui.params_file_name.setText(st)
        startV, endV, points, array_size, idx, nplc, area = get_previous_values()
        if startV is not None and startV:
            self.ui.startV_box.setValue(float(startV))
            pass
        if endV is not None and endV:
            self.ui.endV_box.setValue(float(endV))
            pass
        if points is not None and points:
            self.ui.points_box.setValue(float(points))
            pass
        if array_size is not None and array_size:
            self.ui.array_size_box.setValue(float(array_size))
            pass
        if idx is not None and idx:
            self.ui.device_box.setCurrentIndex(int(idx))
        if nplc is not None and nplc:
            self.ui.nplc_box.setCurrentIndex(int(nplc))
        if area is not None and area:
            self.ui.area_box.setValue(float(area))
        #setup graphs:
        self.prepare_graphs(self.ui.density_graph, 'Voltage', 'V', 'Current', 'A', True)
        self.prepare_graphs(self.ui.power_graph, 'Voltage', 'V', 'Power density', 'W/cm^2', True)
        self.prepare_graphs(self.ui.current_graph, 'Counts', None, 'Current', 'A', False)
        # time observer graphs:
        self.prepare_graphs(self.ui.jscVsTime, 't (min)', None, 'Jsc (mA/cm^2)', None, False)
        self.prepare_graphs(self.ui.UocVsTime, 't (min)', None, 'Uoc', 'V', False)
        self.prepare_graphs(self.ui.FFVsTime, 't (min)', None, 'FF (%)', None, False)
        self.prepare_graphs(self.ui.PCEVsTime, 't (min)', None, 'PCE (%)', None, False)
        self.prepare_graphs(self.ui.jUatThisMoment, 'Voltage', 'V', 'Current', 'A', True)
        self.prepare_graphs(self.ui.PUatThisMoment, 'Voltage', 'V', 'Power density', 'W/cm^2', True)
        self.ui.stepsBox.setEnabled(False)
        self.ui.runingLabel.setStyleSheet("QLabel { background-color : red; color : black; }")
        if (self.ui.device_box.currentText().lower() in "keysight"):
            self.ui.connectUSBbutton.setEnabled(True)
        else:
            self.ui.connectUSBbutton.setEnabled(False)
        #defaults:
        line, dev = get_dev_line()
        if self.ui.usbtmcComboBox.count() > 0 :
            index = self.ui.usbtmcComboBox.findText(dev)
            if index != -1:
                self.ui.usbtmcComboBox.setCurrentIndex(index)
            pass
        #index = self.ui.lineEndingBox.findText(line)
        # self.setWindowIcon()
        #TODO fix default values related to line endings
        l = "win"
        if line == "\r\n":
            l = "Win"
        elif line == "\r":
            l = "Mac"
        elif line == "\n":
            l = "Lin"
        index = self.ui.lineEndingBox.findText(l, QtCore.Qt.MatchContains)
        console(l, line)
        if index != -1:
            self.ui.lineEndingBox.setCurrentIndex(index)
        self.ensure_relays_off()

    def ensure_relays_off(self):
        """
        turns off all relays
        :return:
        """
        try:
            for i in range(1,7):
                print(str(i), " turning off ...")
                relay = RelayToggle(str(i))
                relay.toggle(relay.OFF)
        except Exception as ex:
            print(str(ex))
            console("No raspberry attached, no spur, no local or remote relays?")
        pass


    def select_path(self):
        file = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select a directory to save files to:"))
        if file is not None and file:
            self.ui.directory_path.setPlainText(file)
        pass


    def save_results(self):
        """
        Save parameters only:

        :return:
        """
        suffix = ".dat"
        # file_name = self.ui.name_of_cell.toPlainText()
        params_name = self.ui.params_file_name.text()
        file_path = self.ui.directory_path.toPlainText()
        # full_file = os.path.join(file_path, file_name+'_vach'+suffix)
        params_file = os.path.join(file_path, params_name+'_params'+suffix)
        # console(full_file)
        console(params_file)
        # text = self.ui.vach_text.toPlainText() # all data in one big string
        params_text= self.ui.params_field.toPlainText()
        try:
            # fData = open(full_file, 'w')
            # fData.write(text)
            # fData.close()
            pData= open(params_file, 'w')
            pData.write(params_text)
            pData.close()
            self._params_updated = False # if saved, we do not want to overwrite it again, except they will be updated again
        except Exception as ex:
            console("ERR:FILE:SAVE")
            console(str(ex))
        pass


    def updateCombos(self):
        """
        index is from zero
        :return:
        """
        i = self.ui.relay_combo.currentIndex()
        self.ui.electrode_combo.setCurrentIndex(6-(i+1))
        pass

    def stopExperiment(self):
        """
        Stops experiment
        :return:
        """
        self._worker.stop()
        self.ExpensiveMeter.close()
        self._worker = None
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        self.ui.runingLabel.setText('STOPPED')
        self.ui.runingLabel.setStyleSheet("QLabel { background-color : red; color : black; }")
        self._threads = []
        pass

    def loop_stopped(self, status):
        if status:
            self.ui.startButton.setEnabled(True)
            self.ui.stopButton.setEnabled(False)
            self.ui.runingLabel.setText('STOPPED')
            self.ui.runingLabel.setStyleSheet("QLabel { background-color : red; color : black; }")
            # self._thread = None # ?
            self._threads = []
            pass

    def quit(self):
        try:
            if self._worker is not None:
                self._worker.stop()
            if self.ExpensiveMeter is not None:
                self.ExpensiveMeter.close()
            if self._params_updated: # if parameters were calculated, they will be saved on quit.
                self.save_results()
        except Exception as ex:
            console("ERR.CODE.EXIT")
            console(str(ex))
        sys.exit(0)

    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def MeterConnect(self):
        self.ip = self.ui.ip_address.toPlainText()
        try:
            if self.ui.device_box.currentText().lower() in 'keysight':
                self.ExpensiveMeter = SourceMeter(self.ip)
            elif self.ui.device_box.currentText().lower() in 'keithley':
                self.ExpensiveMeter = SourceMeter_KTHL(self.ip)
                if self.ui.channel_box.currentText().lower() == 'a':
                    self.ExpensiveMeter.setChannel(self.ExpensiveMeter.A)
                    # self.ExpensiveMeter.setBufferSize(self.parameters['array_size'])
                elif self.ui.channel_box.currentText().lower() == 'b':
                    self.ExpensiveMeter.setChannel(self.ExpensiveMeter.B)
                    # self.ExpensiveMeter.setBufferSize(self.parameters['array_size'])
            self.ui.connectionErrorsBox.setPlainText("Connected successfully @"+str(self.ip)+"\nIDN:"+self.ExpensiveMeter.ID)
            self.ui.statusbar.showMessage("@"+str(self.ExpensiveMeter.ID))
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.startButton.setEnabled(True)
            self.updateDevices()
        except Exception as ex:
            # console("ERR.CODE.A")
            # console("wrong IP")
            # console(str(ex))
            traceback.print_exc()
            self.ui.connectionErrorsBox.setPlainText("ERR.CODE.A\nwrong IP\n"+str(ex))

        pass

    def hell(self):
        """
        starts a dialog which starts an experiment
        :return:
        """
        params = self.GetAllParameters()
        # defaults
        path = self.ui.directory_path.toPlainText()
        ip = self.ui.ip_address.toPlainText()
        write_path_ip(path, ip)
        startV = self.ui.startV_box.value()
        endV = self.ui.endV_box.value()
        points = self.ui.points_box.value()
        array_size = self.ui.array_size_box.value()
        dev_idx = self.ui.device_box.currentIndex()
        nplc = self.ui.nplc_box.currentIndex()
        area = self.ui.area_box.value()
        # end of defaults
        dct = {
            'startV':startV,
            'endV':endV,
            'points':points,
            'array_size':array_size,
            'idx':dev_idx,
            'nplc':nplc,
            'area':area
        }
        set_previous_values(dct)
        self.pop_dialog(params)
        pass

    def _clear_t_graphs(self):
        d = self.ui.jscVsTime.listDataItems()
        for i in d:
            self.ui.jscVsTime.removeItem(i)
        d = self.ui.FFVsTime.listDataItems()
        for i in d:
            self.ui.FFVsTime.removeItem(i)
        d = self.ui.UocVsTime.listDataItems()
        for i in d:
            self.ui.UocVsTime.removeItem(i)
        d = self.ui.PCEVsTime.listDataItems()
        for i in d:
            self.ui.PCEVsTime.removeItem(i)


    def startExp(self):
        self.ui.startButton.setEnabled(False)
        self.ui.runingLabel.setText('RUNNING')
        self.ui.runingLabel.setStyleSheet("QLabel { background-color : green; color : black; }")
        self.ui.stopButton.setEnabled(True)
        self.ui.vach_text.setPlainText('U[V] ; I[A] ; j[mA/cm^2] ; P[mW/cm^2]')
        # clear all graph arrays:
        self.curr_array_analysis = []
        self.voltage_array_analysis = []
        self.current_arr = []
        self.voltage_arr = []
        self.t_time_bw = []
        self.t_time_fw = []
        self.ff_time_fw = []
        self.jsc_time_fw = []
        self.Uoc_time_fw = []
        self.PCE_time_fw = []
        self.ff_time_bw = []
        self.jsc_time_bw = []
        self.Uoc_time_bw = []
        self.PCE_time_bw = []
        # self._thread = None
        # for relay-based time observations:
        self._time_c = [[], [], [], [], [], []]
        # no more than 6 relays:
        self._pce_c = [[], [], [], [], [], []]
        self._ff_c = [[], [], [], [], [], []]
        self._jsc_c = [[], [], [], [], [], []]
        self._uoc_c = [[], [], [], [], [], []]
        #clear graphs:
        self._clear_t_graphs()
        self._t1 = datetime.datetime.now()
        # It will allow to start new thread with empty graphs:
        self.parameters = self.GetAllParameters() # we will obtain these values from already updated fields
        mode = self.parameters['mode'] # we will start a particular thread
        if 'keithley' in self.ExpensiveMeter.ID.lower():
            self.ExpensiveMeter.setBufferSize(self.parameters['array_size'])
            self.ExpensiveMeter.setSourceOutputMode('volt')
            self.ExpensiveMeter.setMeasurementMode(1)
            if self.ui.channel_box.currentText().lower() == 'a':
                self.ExpensiveMeter.setChannel(self.ExpensiveMeter.A)
                # self.ExpensiveMeter.setBufferSize(self.parameters['array_size'])
            elif self.ui.channel_box.currentText().lower() == 'b':
                self.ExpensiveMeter.setChannel(self.ExpensiveMeter.B)
            # self.ExpensiveMeter.setCurrentLimit(self.parameters['limitA'])
            console('limitA', self.parameters['limitA'])
        self._thread = QThread(self) # why??? WHY????
        self._thread.setObjectName("WLoop")
        if mode == 0:
            self._worker = LoopWorker(self.ExpensiveMeter, **self.parameters)
            self._worker.moveToThread(self._thread)
            self._worker.current_results.connect(self.draw_graph)
            self._worker.final.connect(self.loop_stopped)
            self._worker.trigger.connect(self.calculate_param)
            self._worker.errors.connect(self.ErrorHasBeenGot)
            self._worker.progress.connect(self.ExperimentInfo)
        elif mode == 1:
            console("TIME MODE")
            self._worker = ContinuousObserver(self.ExpensiveMeter, **self.parameters)
            self._worker.moveToThread(self._thread)
            # TODO: correct all signals!
            self._worker.current_results.connect(self.draw_time_graph)
            self._worker.final.connect(self.loop_stopped)
            self._worker.trigger.connect(self.calculate_param)
            self._worker.errors.connect(self.ErrorHasBeenGot)
            self._worker.progress.connect(self.ExperimentInfo)
        elif mode == 2:
            self.delete_graph()
            console("RELAY MODE")
            self._worker = RelayObserver(self.ExpensiveMeter, **self.parameters)
            self._worker.moveToThread(self._thread)
            self._worker.current_results.connect(self.draw_graph_relay)
            self._worker.final.connect(self.loop_stopped)
            self._worker.trigger.connect(self.calculate_param)
            self._worker.errors.connect(self.ErrorHasBeenGot)
            self._worker.progress.connect(self.ExperimentInfo)
            pass
        elif mode == 3:
            self.delete_graph()
            console("RELAY TIME MODE")
            self._worker = RelayCO(self.ExpensiveMeter, **self.parameters)
            self._worker.moveToThread(self._thread)
            self._worker.current_results.connect(self.draw_graph_time_relay)
            self._worker.final.connect(self.loop_stopped)
            self._worker.trigger.connect(self.calculate_param)
            self._worker.errors.connect(self.ErrorHasBeenGot)
            self._worker.progress.connect(self.ExperimentInfo)
            pass
        else:
            console("WTF IN THIS LINE?")
            console('mode', mode)
            sys.exit(-127)
        self._thread.started.connect(self._worker.run)
        self._thread.start()
        pass

    def ExperimentInfo(self, string):
        self.ui.real_data_output.appendPlainText(string)
        pass

    def ErrorHasBeenGot(self, i, string):
        self.ui.connectionErrorsBox.appendPlainText(string)
        pass

    def setMode(self, mode):
        """
        Sets measurement mode

        
        :param mode:
        :return:
        """
        if mode == 0:
            self.ui.oneShotMode.setChecked(True)
        elif mode == 1:
            self.ui.timeMode.setChecked(True)
            pass
        elif mode == 2:
            self.ui.relayMode.setChecked(True)
            pass
        elif mode == 3:
            self.ui.timeMode_2.setChecked(True)
        pass

    def getMode(self):
        """

        :return: one contact mode 0, time mode 1, relay mode 2
        """
        mode = 0 # default 0, time mode 1, relay mode 2
        if self.ui.timeMode.isChecked():
            mode = 1
        elif self.ui.relayMode.isChecked():
            mode=2
        elif self.ui.timeMode_2.isChecked():
            mode=3
        elif self.ui.oneShotMode.isChecked():
            mode =0
        else:
            mode =0
        return mode
        pass

    def return_start_stop_fn(self):
        startV = self.ui.startV_box.value()
        endV = self.ui.endV_box.value()
        mn = min(startV, endV)
        mx = max(startV, endV)
        return mx, mn

    def GetAllParameters(self):
        """

        :return:
        """
        # startV = self.ui.startV_box.value()
        # endV = self.ui.endV_box.value()
        startV, endV = self.return_start_stop_fn()
        points = self.ui.points_box.value()
        current_limit = self.ui.limitA_box.value()
        wait = self.ui.wait_box.value()
        array_size = self.ui.array_size_box.value()
        x_mean = self.ui.x_mean_box.value()
        el_area = self.ui.area_box.value() # in mm^2 !!!!
        in_power = self.ui.power_input_box.value()
        fb_scan = self.ui.fb_scan.checkState()
        dark_scan=self.ui.darkBox.checkState()
        relay_combo = self.ui.relay_combo.currentIndex()
        el_combo = self.ui.electrode_combo.currentIndex()
        sc_name =  self.ui.name_of_cell.toPlainText()
        mode = self.getMode()
        delay_min = self.ui.timeDelayBox.value()
        counts = self.ui.countBox.value()
        nplc = self.ui.nplc_box.currentText()
        use_relay = self.ui.chooseRel.isChecked()
        parameters = {'startV': startV,
                      'endV': endV,
                      'points': points,
                      'limitA': current_limit,
                      'wait': wait,
                      'array_size': array_size,
                      'x_mean': x_mean,
                      'area': el_area,
                      'in_power': in_power,
                      'fb_scan': fb_scan,
                      'dark_scan':dark_scan,
                      'relay_combo':relay_combo,
                      'el_combo': el_combo,
                      'sc_name':sc_name,
                      'mode':mode,
                      'delay_min':delay_min,
                      'counts':counts,
                      'nplc': nplc,
                      'cRel':use_relay
                      }
        return parameters
        pass


    def calculate_param(self, trigger, fb_scan, counter, name='', c=1):
        """
        o kur grafikai paišomi?
        :return:
        """
        console(self.parameters['mode'], ' : MODE')
        self._t2 = datetime.datetime.now()
        self._t_diff = self._t2 - self._t1
        t_min = round((self._t_diff.seconds/60.0), 2)
        params_dict = {}
        if(trigger):
            # t_min = 0
            self._params_updated = True
            if(fb_scan):
                # BW section
                #     forward direction
                self.ui.fbStatusLabel.setText("BW scan")
                V_oc = self.voltage_array_analysis[closestValueIndex(self.curr_array_analysis, 0)]
                I_sc = self.curr_array_analysis[closestValueIndex(self.voltage_array_analysis, 0)]
                j_sc = (I_sc*1000/self.parameters['area'])*100 #mA/cm^2
                # Update values in LCDs:
                # TODO: update LCDs and clear arrays:
                p_max, I_max, U_max = getMaxPJV(self.curr_array_analysis, self.voltage_array_analysis)
                #
                ff = getFF(p_max*1000/self.parameters['area']*100, V_oc, j_sc) # W => mW
                pce = getPCE(p_max*1000/self.parameters['area']*100, self.parameters['in_power']) # as well as here
                self.ExperimentInfo("========STATS=========")
                self.ExperimentInfo('p_max array length: '+str(len(self.curr_array_analysis))+ " , "+str(len(self.voltage_array_analysis)))
                self.ExperimentInfo('V_oc: ' + str(V_oc) + '\n' + 'I_sc: ' + str(I_sc) + '\n' + 'PCE: ' + str(
                    pce) + '\n' + 'FF: ' + str(ff))
                self.ExperimentInfo('j sc: '+str(j_sc))
                self.ExperimentInfo("P max: " + str(p_max) + "\nI_max: " + str(I_max) + "\nU_max: " + str(U_max))
                self.ExperimentInfo("===END OF STATS===")
                if self.parameters['mode'] == 0 or self.parameters['mode'] == 2:
                    params_dict = {
                        'v_oc': round(V_oc, 5),
                        'j_sc': round(j_sc, 5),
                        'I_sc': round(I_sc, 5),
                        'Imax': round(I_max, 7),
                        'ff': round(ff, 4),
                        'pce': round(pce, 4),
                        'pmax': round(p_max / self.parameters['area'] * 1000 * 100, 4),  # P max in mW/cm^2
                        'vmax': round(U_max, 4),
                        'fb_scan': fb_scan,
                        't_min': counter
                    }
                elif self.parameters['mode'] == 1: #self.parameters['mode'] == 3:
                    console("Mode from elif", self.parameters['mode'])
                    #t_min = counter*self.ui.timeDelayBox.value()
                    params_dict = {
                        'v_oc': round(V_oc, 5),
                        'j_sc': round(j_sc, 5),
                        'I_sc': round(I_sc, 5),
                        'Imax': round(I_max, 7),
                        'ff': round(ff, 4),
                        'pce': round(pce, 4),
                        'pmax': round(p_max / self.parameters['area'] * 1000 * 100, 4),  # P max in mW/cm^2
                        'vmax': round(U_max, 4),
                        'fb_scan': fb_scan,
                        't_min': t_min
                    }
                    self.t_time_bw.append(t_min)
                    self.PCE_time_bw.append(pce)
                    self.jsc_time_bw.append(j_sc)
                    self.Uoc_time_bw.append(round(V_oc,5))
                    self.ff_time_bw.append(ff)
                elif self.parameters['mode'] == 3: #self.parameters['mode'] == 3:
                    console("Mode from elif", self.parameters['mode'])
                    #t_min = counter*self.ui.timeDelayBox.value()
                    params_dict = {
                        'v_oc': round(V_oc, 5),
                        'j_sc': round(j_sc, 5),
                        'I_sc': round(I_sc, 5),
                        'Imax': round(I_max, 7),
                        'ff': round(ff, 4),
                        'pce': round(pce, 4),
                        'pmax': round(p_max / self.parameters['area'] * 1000 * 100, 4),  # P max in mW/cm^2
                        'vmax': round(U_max, 4),
                        'fb_scan': fb_scan,
                        't_min': t_min
                    }
                    # append measurement data:
                    # c indicates relay's number and array's index also:
                    self._time_c[c-1].append(t_min)
                    self._pce_c[c-1].append(pce)
                    self._ff_c[c-1].append(ff)
                    self._jsc_c[c-1].append(j_sc)
                    self._uoc_c[c-1].append(V_oc)
                self.upload_values(params_dict, name)
                self.ui.pceLCD.setValue(pce)
                self.ui.jscLCD.setValue(j_sc)
                self.ui.uocLCD.setValue(V_oc)
                self.ui.ffLCD.setValue(ff)
                # clearing of arrays
                self.curr_array_analysis = []
                self.voltage_array_analysis = []
                # TODO: save measurement data
                file_name = self.ui.name_of_cell.toPlainText()+'_BW_'+str(t_min)+name+'.dat'
                file_path = self.ui.directory_path.toPlainText()
                file = os.path.join(file_path, file_name)
                text = self.ui.vach_text.toPlainText()
                try:
                    writer = open(file, 'w')
                    writer.write(text)
                    writer.close()
                except Exception as ex:
                    console("ERR:WRITE FW")
                    console(str(ex))
                    pass
                # todo: clear data:
                self.ui.vach_text.setPlainText('U[V] ; I[A] ; j[mA/cm^2] ; P[mW/cm^2]')
                pass
            elif not fb_scan:
                self.ui.fbStatusLabel.setText("FW scan")
                V_oc = self.voltage_array_analysis[closestValueIndex(self.curr_array_analysis, 0)]
                I_sc = self.curr_array_analysis[closestValueIndex(self.voltage_array_analysis, 0)]
                j_sc = (I_sc*1000 / self.parameters['area'])*100
                # Update values in LCDs:
                # TODO: update LCDs and clear arrays:
                p_max, I_max, U_max = getMaxPJV(self.curr_array_analysis, self.voltage_array_analysis)
                ff = getFF(p_max*1000/self.parameters['area']*100, V_oc, j_sc)
                pce = getPCE(p_max*1000/self.parameters['area']*100, self.parameters['in_power'])
                self.ExperimentInfo("========STATS=========")
                self.ExperimentInfo('V_oc: '+ str(V_oc) + '\n' +'I_sc: '+str(I_sc)+'\n'+'PCE: '+str(pce)+'\n'+'FF: '+str(ff)+ '\n')
                self.ExperimentInfo('j sc: ' + str(j_sc))
                self.ExperimentInfo("P max: "+str(p_max)+"\nI_max: "+str(I_max)+"\nU_max: "+str(U_max))
                self.ExperimentInfo("===END OF STATS===")
                if self.parameters['mode'] == 0 or self.parameters['mode'] == 2:
                    params_dict = {
                        'v_oc': round(V_oc, 5),
                        'j_sc': round(j_sc, 5),
                        'I_sc': round(I_sc, 5),
                        'Imax': round(I_max, 7),
                        'ff': round(ff, 4),
                        'pce': round(pce, 4),
                        'pmax': round(p_max / self.parameters['area'] * 1000 * 100, 4),  # P max in mW/cm^2
                        'vmax': round(U_max, 4),
                        'fb_scan': fb_scan,
                        't_min': counter
                    }
                elif self.parameters['mode'] == 1:# or self.parameters['mode'] == 3:
                    console("Mode from FW elif", self.parameters['mode'])
                    #t_min = counter*self.ui.timeDelayBox.value()
                    params_dict = {
                        'v_oc': round(V_oc, 5),
                        'j_sc': round(j_sc, 5),
                        'I_sc': round(I_sc, 5),
                        'Imax': round(I_max, 7),
                        'ff': round(ff, 4),
                        'pce': round(pce, 4),
                        'pmax': round(p_max / self.parameters['area'] * 1000 * 100, 4),  # P max in mW/cm^2
                        'vmax': round(U_max, 4),
                        'fb_scan': fb_scan,
                        't_min': t_min
                    }
                    self.t_time_fw.append(t_min)
                    self.PCE_time_fw.append(pce)
                    self.jsc_time_fw.append(j_sc)
                    self.Uoc_time_fw.append(round(V_oc,5))
                    self.ff_time_fw.append(ff)
                elif self.parameters['mode'] == 3: #self.parameters['mode'] == 3:
                    console("Mode from elif, FW fork: ", self.parameters['mode'])
                    #t_min = counter*self.ui.timeDelayBox.value()
                    params_dict = {
                        'v_oc': round(V_oc, 5),
                        'j_sc': round(j_sc, 5),
                        'I_sc': round(I_sc, 5),
                        'Imax': round(I_max, 7),
                        'ff': round(ff, 4),
                        'pce': round(pce, 4),
                        'pmax': round(p_max / self.parameters['area'] * 1000 * 100, 4),  # P max in mW/cm^2
                        'vmax': round(U_max, 4),
                        'fb_scan': fb_scan,
                        't_min': t_min
                    }
                    # append measurement data:
                    # c indicates relay's number and array's index also:
                    self._time_c[c].append(t_min)
                    self._pce_c[c].append(pce)
                    self._ff_c[c].append(ff)
                    self._jsc_c[c].append(j_sc)
                    self._uoc_c[c].append(V_oc)
                self.upload_values(params_dict, name)
                #     LCDs:
                self.ui.pceLCD.setValue(pce)
                self.ui.jscLCD.setValue(j_sc)
                self.ui.uocLCD.setValue(V_oc)
                self.ui.ffLCD.setValue(ff)
                # clearing of arrays
                self.curr_array_analysis = []
                self.voltage_array_analysis = []
                # TODO: save measurement data
                file_name = self.ui.name_of_cell.toPlainText() + '_FW_'+str(t_min)+name+'.dat'
                file_path = self.ui.directory_path.toPlainText()
                file = os.path.join(file_path, file_name)
                text = self.ui.vach_text.toPlainText()
                try:
                    writer = open(file, 'w')
                    writer.write(text)
                    writer.close()
                except Exception as ex:
                    console("ERR:WRITE BW")
                    console(str(ex))
                    pass
                # todo: clear data:
                self.ui.vach_text.setPlainText('U[V] ; I[A] ; j[mA/cm^2] ; P[mW/cm^2]')
                pass
            else:
                console("ERR:CODE:SHIT_HAPPENED AGAIN")
                console(trigger, fb_scan, " VALUES")
            # here we will plot all time dpendencies:
            console("MODE:",self.parameters['mode'])
            if self.parameters['mode'] == 1:
                self.update_graph(self.ui.PCEVsTime, self.t_time_fw, self.PCE_time_fw, "FWPCE", color=self.GREEN)
                self.update_graph(self.ui.PCEVsTime, self.t_time_bw, self.PCE_time_bw, "BWPCE", color=self.RED)
                self.update_graph(self.ui.jscVsTime, self.t_time_fw, self.jsc_time_fw, "FWJSC", color=self.GREEN)
                self.update_graph(self.ui.jscVsTime, self.t_time_bw, self.jsc_time_bw, "BWJSC", color=self.RED)
                self.update_graph(self.ui.UocVsTime, self.t_time_fw, self.Uoc_time_fw, "FWUOC", color=self.GREEN)
                self.update_graph(self.ui.UocVsTime, self.t_time_bw, self.Uoc_time_bw, "BWUOC", color=self.RED)
                self.update_graph(self.ui.FFVsTime, self.t_time_fw, self.ff_time_fw, "FWFF", color=self.GREEN)
                self.update_graph(self.ui.FFVsTime, self.t_time_bw, self.ff_time_bw, "BWFF", color=self.RED)
            elif self.parameters['mode'] == 3:
                console("3'rd case")
                #================================================
                # self.update_graph(self.ui.PCEVsTime, self.t_time_fw, self.PCE_time_fw, "FWPCE", color=self.color[c])
                # self.update_graph(self.ui.jscVsTime, self.t_time_fw, self.jsc_time_fw, "FWJSC", color=self.color[c])
                # self.update_graph(self.ui.UocVsTime, self.t_time_fw, self.Uoc_time_fw, "FWUOC", color=self.color[c])
                # self.update_graph(self.ui.FFVsTime, self.t_time_fw, self.ff_time_fw, "FWFF", color=self.color[c])
                #================================================
                for i in range(0,6):
                    t_arr = self._time_c[i]
                    pce_arr = self._pce_c[i]
                    jsc_arr = self._jsc_c[i]
                    uoc_arr = self._uoc_c[i]
                    ff_arr = self._ff_c[i]
                    if len(t_arr) > 0 and len(pce_arr) > 0 and len(jsc_arr) > 0 and len(uoc_arr) > 0 and len(ff_arr) > 0:
                        self.update_graph(self.ui.PCEVsTime, t_arr, pce_arr, "FWPCE"+str(i), color=self.color[i])
                        self.update_graph(self.ui.jscVsTime, t_arr, jsc_arr, "FWJSC"+str(i), color=self.color[i])
                        self.update_graph(self.ui.UocVsTime, t_arr, uoc_arr, "FWUOC"+str(i), color=self.color[i])
                        self.update_graph(self.ui.FFVsTime, t_arr, ff_arr, "FWFF"+str(i), color=self.color[i])
                        pass
        else:
            console("ERR:CODE:über shit")
            console(trigger, " trig value")
        pass

    def upload_values(self, params_dict, name=''):
        fb = "FW"
        if params_dict['fb_scan']:
            fb = "BW"
        elif not params_dict['fb_scan']:
            fb="FW"
        sc_name = self.ui.name_of_cell.toPlainText()
        # contruct strings to write down:
        a1 = sc_name+name + " ; "+fb+" ; "+str(params_dict['v_oc'])+" ; "
        a2 = str(params_dict['j_sc'])+ " ; "+str(params_dict['ff'])+ " ; "+str(params_dict['vmax'])+" ; "
        a3 = str(params_dict['Imax']*1000*100/self.parameters['area'])+ " ; "+str(params_dict['pmax'])+" ; "
        a4 = str(params_dict['pce'])+" ; "+str(self.parameters['area']/100)+" ; "+str(params_dict['t_min'])
        self.ui.params_field.append(a1+a2+a3+a4)
        if self.parameters['mode'] == 1:
            self.save_results()
            pass
        pass

    def draw_graph(self, status, fb_scan, data_mean, err_rate, totalV, curr_array, name):
        """

        :param status:
        :param fb_scan:
        :param data_mean:
        :param err_rate:
        :param totalV:
        :param curr_array:
        :return:
        """

        self.ExperimentInfo('Current '+ str(round(data_mean, 7))+"\n"+'U : '+str(round(totalV, 4)))
        self.ui.live_error.setText(str(round(err_rate, 5)))
        array = np.arange(0, self.parameters['array_size'], 1)
        self.draw_method(self.ui.current_graph,  array, curr_array, clear=True)
        if status:
            self.current_arr.append(data_mean)
            self.curr_array_analysis.append(data_mean)
            self.voltage_arr.append(totalV)
            self.voltage_array_analysis.append(totalV)
            self.append_jV_values(data_mean, totalV, self.parameters['area'])
            self.density_arr = [(x / self.parameters['area'])*100 for x in self.current_arr]
            self.power_arr = [a * b for a,b in zip(self.density_arr, self.voltage_arr)]
            self.update_graph(self.ui.density_graph,  self.voltage_arr, self.current_arr, name, color=self.BLUE)
            self.update_graph(self.ui.power_graph,  self.voltage_arr, self.power_arr, name, color=self.SKYBLUE)
        pass

    def draw_time_graph(self, status, fb_scan, data_mean, err_rate, totalV, curr_array):
        """

        :param status:
        :param fb_scan:
        :param data_mean:
        :param err_rate:
        :param totalV:
        :param curr_array:
        :return:
        """
        self.ExperimentInfo('Current '+ str(round(data_mean, 7))+"\n"+'U : '+str(round(totalV, 4)))
        self.ui.live_error.setText(str(round(err_rate, 5)))
        array = np.arange(0, self.parameters['array_size'], 1)
        self.draw_method(self.ui.current_graph,  array, curr_array, clear=True)
        if status:
            # self.current_arr.append(data_mean)
            self.curr_array_analysis.append(data_mean)
            # self.voltage_arr.append(totalV)
            self.voltage_array_analysis.append(totalV)
            self.append_jV_values(data_mean, totalV, self.parameters['area'])
            self.density_arr = [(x / self.parameters['area'])*100 for x in self.curr_array_analysis]
            self.power_arr = [a * b for a,b in zip(self.density_arr, self.voltage_array_analysis)]
            self.update_graph(self.ui.jUatThisMoment,  self.voltage_array_analysis, self.curr_array_analysis, 'Current', color=self.BLUE)
            self.update_graph(self.ui.PUatThisMoment,  self.voltage_array_analysis, self.power_arr, 'Power', color=self.SKYBLUE)
        pass

    def draw_graph_relay(self, status, fb_scan, data_mean, err_rate, totalV, curr_array, name, wipe, c):
        """

        :param status:
        :param fb_scan:
        :param data_mean:
        :param err_rate:
        :param totalV:
        :param curr_array:
        :return:
        """
        if wipe:
            self.curr_array_analysis = []
            self.voltage_array_analysis = []
            self.current_arr = []
            self.voltage_arr = []
        else:
            self.ExperimentInfo('Current '+ str(round(data_mean, 7))+"\n"+'U : '+str(round(totalV, 4)))
            self.ui.live_error.setText(str(round(err_rate, 5)))
            array = np.arange(0, self.parameters['array_size'], 1)
            self.draw_method(self.ui.current_graph,  array, curr_array, clear=True)
            if status:
                self.current_arr.append(data_mean)
                self.curr_array_analysis.append(data_mean)
                self.voltage_arr.append(totalV)
                self.voltage_array_analysis.append(totalV)
                self.append_jV_values(data_mean, totalV, self.parameters['area'])
                self.density_arr = [(x / self.parameters['area'])*100 for x in self.current_arr]
                self.power_arr = [a * b for a,b in zip(self.density_arr, self.voltage_arr)]
                self.update_graph(self.ui.density_graph,  self.voltage_arr, self.current_arr, name, color=self.color[c])
                self.update_graph(self.ui.power_graph,  self.voltage_arr, self.power_arr, name, color=self.color[c])
            pass


    def draw_graph_time_relay(self, status, fb_scan, data_mean, err_rate, totalV, curr_array, name, wipe, c):
        """

        :param status:
        :param fb_scan:
        :param data_mean:
        :param err_rate:
        :param totalV:
        :param curr_array:
        :return:
        """
        if wipe:
            self.curr_array_analysis = []
            self.voltage_array_analysis = []
            self.current_arr = []
            self.voltage_arr = []
        else:
            self.ExperimentInfo('Current '+ str(round(data_mean, 7))+"\n"+'U : '+str(round(totalV, 4)))
            self.ui.live_error.setText(str(round(err_rate, 5)))
            array = np.arange(0, self.parameters['array_size'], 1)
            self.draw_method(self.ui.current_graph,  array, curr_array, clear=True)
            if status:
                self.current_arr.append(data_mean)
                self.curr_array_analysis.append(data_mean)
                self.voltage_arr.append(totalV)
                self.voltage_array_analysis.append(totalV)
                self.append_jV_values(data_mean, totalV, self.parameters['area'])
                self.density_arr = [(x / self.parameters['area'])*100 for x in self.current_arr]
                self.power_arr = [a * b for a,b in zip(self.density_arr, self.voltage_arr)]
                self.update_graph(self.ui.jUatThisMoment,  self.voltage_arr, self.current_arr, name, color=self.color[c])
                self.update_graph(self.ui.PUatThisMoment,  self.voltage_arr, self.power_arr, name, color=self.color[c])
            pass

    def append_jV_values(self, I, V, area):
        """
        Appends i, V, j, P values into vach_text field:

        :param I:
        :param V:
        :param area:
        :return:
        """
        j = I*1000 / (area/100) # mm^2 => cm^2, A => mA
        P = j*V
        self.ui.vach_text.append(str(round(V, 7))+" ; "+str(round(I,7))+" ; "+str(round(j,7))+" ; "+str(round(P,7))) # there is no need to add a newline
        pass


    def prepare_graphs(self, graph:pg.PlotWidget, x_title, x_scale, y_title, y_scale, xy00=False):
        # graph.clear()
        graph.setBackground((47,79,79))
        if x_scale is not None:
            graph.setLabel('bottom', x_title, units=str(x_scale))
        else:
            graph.setLabel('bottom', x_title)
        if y_scale is not None:
            graph.setLabel('left', y_title, units=str(y_scale))
        else:
            graph.setLabel('left', y_title)
        graph.getAxis('bottom').setPen((255, 255, 255))
        graph.getAxis('left').setPen((255, 255, 255))
        # graph.plot(x, y, pen=(255,255,102), symbol='o')
        graph.showGrid(x=True,y=True)
        if xy00:
            y0 = graph.addLine(None, 0, None)
            x0 = graph.addLine(0, None, None)
            y0.setPen(mkPen('y', width=3))
            x0.setPen(mkPen('y', width=3))

    def draw_method(self, graph:pg.PlotWidget, x, y, y1=None, datasets=None, clear = False):
        if clear:
            graph.clear()
        graph.plot(x, y, pen=(255, 255, 102), symbol='o')
        if y1 is not None and len(y1)>0:
            graph.plot(x, y1, pen=(255,255, 186), symbol='o')
        if datasets is not None:
            for i in datasets:
                graph.plot(x, i, pen=(randint(0,255), randint(0,255), randint(0,255)), symbol='o')


    def update_graph_complex(self, graph:pg.PlotWidget, x, y, y_name, y1=None, datasets=None, clear = False, y2_name=None, names=None):
        if clear:
            dataItems = graph.listDataItems()
            for i in dataItems:
                console(i.name())
                if i is not None:
                    if i.name() == y_name:
                        graph.removeItem(i)
                    if y2_name is not None:
                        if i.name() == y2_name:
                            graph.removeItem(i)
        graph.plot(x, y, pen=(255, 255, 102), symbol='o', name=y_name)
        if y1 is not None and len(y1)>0:
            graph.plot(x, y1, pen=(255,255, 186), symbol='o', name=y2_name)
        if datasets is not None:
            for i in datasets:
                graph.plot(x, i, pen=(randint(0,255), randint(0,255), randint(0,255)), symbol='o')

    def update_graph(self, graph:pg.PlotWidget, x, y, y_name, color=(255, 255, 102)):
        """
        Updates a graph
        :param graph: plotWidget
        :param x: x dataset
        :param y: y dataset
        :param y_name: name (MUST)
        :param color: default: 255, 255, 102
        :return:
        """
        sizex = len(x)
        sizey=len(y)
        # console("Upd. graph triggered")
        if sizex == sizey:
            dataItems =  graph.listDataItems()
            for i in dataItems:
                # console(i.name(), " ", y_name)
                if i is not None:
                    if i.name() == y_name:
                        graph.removeItem(i)
            graph.plot(x,y, pen=color, symbol='o', name=y_name, symbolBrush=color)
        else:
            console("Inequality", y_name, " ; ", sizex, " ; ", sizey)

    def delete_graph(self):
        dataItems1 = self.ui.density_graph.listDataItems()
        for i in dataItems1:
            self.ui.density_graph.removeItem(i)

        dataItems2 = self.ui.power_graph.listDataItems()
        for i in dataItems2:
            self.ui.power_graph.removeItem(i)

    def pop_dialog(self, params):
        self.dialog = PopUp(params)
        if self.dialog.exec_():
            self.dialog.ui.array_size_box.setMaximum(self.max_array)
            parameters = self.dialog.GetAllParameters()
            self.ui.startV_box.setValue(parameters['startV'])
            self.ui.endV_box.setValue(parameters['endV'])
            self.ui.points_box.setValue(parameters['points'])
            self.ui.limitA_box.setValue(parameters['limitA'])
            self.ui.wait_box.setValue(parameters['wait'])
            self.ui.array_size_box.setValue(parameters['array_size'])
            self.ui.x_mean_box.setValue(parameters['x_mean'])
            self.ui.area_box.setValue(parameters['area'])
            self.ui.power_input_box.setValue(parameters['in_power'])
            self.ui.fb_scan.setCheckState(parameters['fb_scan'])
            self.ui.darkBox.setCheckState(parameters['dark_scan'])
            # TODO: ComboBoxes are left, need to implement:
            # relay_combo = self.ui.relay_combo.currentText()
            # console("RELAY:", parameters['relay_combo'])
            self.ui.relay_combo.setCurrentIndex(parameters['relay_combo'])
            # console(self.ui.relay_combo.currentIndex())
            # el_combo = self.ui.electrode_combo.currentText()
            self.ui.electrode_combo.setCurrentIndex(parameters['el_combo'])
            self.ui.name_of_cell.setPlainText(parameters['sc_name'])
            self.setMode(parameters['mode'])
            self.ui.timeDelayBox.setValue(parameters['delay_min'])
            self.ui.countBox.setValue(parameters['counts'])
            self.ui.chooseRel.setChecked(parameters['cRel'])
            # console("done")
            if not self._demo_:
                self.startExp()