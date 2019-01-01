from PyQt5 import QtWidgets, QtGui
from GUI.Solar import Ui_MainWindow
from GUI.Dialog import Ui_SettingsDialog
import sys
from PyQt5.QtCore import *
from HardwareAccess.KeysightWrapper import SourceMeter
from ExpLoop import *



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ThreadPool = QThreadPool()
        # self._threads = []
        self._thread = None
        self._worker = None
        self._path = None
        self.ExpensiveMeter = None
        self.ip = None
        self.jvView = self.ui.density_graph
        self.ui.connect_button.clicked.connect(self.MeterConnect)
        self.ui.startButton.clicked.connect(self.hell)
        self.ui.quitButton.clicked.connect(self.quit)
        self.ui.save_as_button.clicked.connect(self.add_Chapayev_constant)
        self.ui.fullscreenButton.clicked.connect(self.fullscreen)
        self.ui.stopButton.clicked.connect(self.stopExperiment)
        self.ui.actionQuit.triggered.connect(self.quit)

        self.parameters = {}
        self.current_arr = []
        self.voltage_arr = []
    #     Shortcuts:
        self.quit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence( "Ctrl+Q" ), self)
        # events of shortcuts:
        self.quit_shortcut.activated.connect(self.quit)

    #     Plots:
        self.density_graph = self.ui.density_graph.plot()
        self.current_graph = self.ui.current_graph.plot()

    def stopExperiment(self):
        """
        Stops experiment
        :return:
        """
        self._worker.stop()
        self.ui.startButton.setEnabled(True)
        self.ui.stopButton.setEnabled(False)
        pass

    def quit(self):
        try:
            if self._worker is not None:
                self._worker.stop()
            if self.ExpensiveMeter is not None:
                self.ExpensiveMeter.close()
        except Exception as ex:
            print("ERR.CODE.EXIT")
            print(str(ex))
        sys.exit(0)

    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def MeterConnect(self):
        self.ip = self.ui.ip_address.toPlainText()
        try:
            self.ExpensiveMeter = SourceMeter(self.ip)
            self.ui.connectionErrorsBox.setPlainText("Connected successfully @"+str(self.ip))
            self.ui.tabWidget.setCurrentIndex(0)
            self.ui.startButton.setEnabled(True)
        except Exception as ex:
            # print("ERR.CODE.A")
            # print("wrong IP")
            # print(str(ex))
            self.ui.connectionErrorsBox.setPlainText("ERR.CODE.A\nwrong IP\n"+str(ex))
        pass

    def hell(self):
        params = self.GetAllParameters()
        self.pop_dialog(params)
        pass

    def startExp(self):
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        # TODO: here is a mistake - we need to reorder the logic how we retrieve all
        #  TODO: necessary parameters
        # self.parameters = {} # DO not clear dict!
        self.parameters = self.GetAllParameters() # we will obtain these values from already updated fields
        self._thread = QThread()
        self._thread.setObjectName("WLoop")
        self._worker = LoopWorker(self.ExpensiveMeter, **self.parameters)
        self._worker.moveToThread(self._thread)
        # self._worker.results.connect(self.draw_I)
        self._worker.current_results.connect(self.draw_graph)
        # self._worker.final.connect(self.calculate_param)
        self._worker.trigger.connect(self.calculate_param)
        self._worker.errors.connect(self.ErrorHasBeenGot)
        #self._worker.progress.connect(self.ExperimentInfo)
        self._thread.started.connect(self._worker.run)
        self._thread.start()
        pass

    def ErrorHasBeenGot(self, i, string):
        self.ui.connectionErrorsBox.appendPlainText(string)
        pass

    def GetAllParameters(self):
        """

        :return:
        """
        startV = self.ui.startV_box.value()
        endV = self.ui.endV_box.value()
        points = self.ui.points_box.value()
        current_limit = self.ui.limitA_box.value()
        wait = self.ui.wait_box.value()
        array_size = self.ui.array_size_box.value()
        x_mean = self.ui.x_mean_box.value()
        el_area = self.ui.area_box.value()
        in_power = self.ui.power_input_box.value()
        fb_scan = self.ui.fb_scan.checkState()
        relay_combo = self.ui.relay_combo.currentIndex()
        el_combo = self.ui.electrode_combo.currentIndex()


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
                      'relay_combo':relay_combo,
                      'el_combo': el_combo}
        return parameters
        pass

    def calculate_param(self, trigger, fb_scan):
        # TODO: implement triggered analysis

        """

        :return:
        """
        if(trigger):
            if(fb_scan):
                pass
            elif not fb_scan:
                pass
            else:
                print("ERR:CODE:SHIT_HAPPENED AGAIN")
                print(trigger, fb_scan, " VALUES")
        else:
            print("ERR:CODE:über shit")
            print(trigger, " trig value")
        pass

    def draw_graph(self, status, fb_scan, data_mean, err_rate, totalV, curr_array):
        """

        :param status:
        :param fb_scan:
        :param data_mean:
        :param err_rate:
        :param totalV:
        :param curr_array:
        :return:
        """
        print('status', status)
        print('current_mean', data_mean)
        print('err_rate', err_rate)
        print('totalV', totalV)
        self.ui.live_error.setText(str(round(err_rate, 3)))
        array = np.arange(0, self.parameters['array_size'], 1)
        self.draw_method(self.ui.current_graph, '6th dimension', 'a.u.', 'Current', 'A', array, curr_array)
        if status:
            self.current_arr.append(data_mean)
            self.voltage_arr.append(totalV)
            self.density_arr = [x / self.parameters['area'] for x in self.current_arr]
            self.power_arr = [a * b for a,b in zip(self.density_arr, self.voltage_arr)]
            self.draw_method(self.ui.density_graph, 'Voltage', 'V', 'Current', 'A', self.voltage_arr, self.current_arr)
            self.draw_method(self.ui.power_graph, 'Voltage', 'V', 'Power density', 'W/cm^2', self.voltage_arr, self.power_arr)
        pass

    def add_Chapayev_constant(self):
        text = ["U"]
        self.ui.vach_text.append("blah, ha ha ha")

        pass

    def draw_JV(self, x, y):
        self.draw_method(self.ui.density_graph, 'Voltage', 'V', 'Current density', 'A/cm^2', x, y)
        pass

    def draw_I(self, x, y):
        array = np.arange(0, x, 1)
        self.draw_method(self.ui.current_graph,  '6th dimension', 'a.u.', 'Current', 'A' , array, y)
        pass

    def draw_P(self, x ,y):
        self.draw_method(self.ui.power_graph, 'Voltage', 'V', 'Power density', 'W/cm^2', x, y)
        pass

    def draw_method(self, graph, x_title, x_scale, y_title, y_scale, x, y):
        graph.clear()
        graph.setBackground((47,79,79))
        graph.setLabel('bottom', x_title, x_scale)
        graph.setLabel('left', y_title, y_scale)
        graph.getAxis('bottom').setPen((255, 255, 255))
        graph.getAxis('left').setPen((255, 255, 255))
        graph.plot(x, y, pen=(255,255,102), symbol='o')
        graph.showGrid(x=True,y=True)

    def updateQLCD(self, lcd, value):
        palette = self.ui.lcdNumber.palette()
        # foreground color
        palette.setColor(palette.WindowText, QtGui.QColor(255, 255, 255))
        # background color
        palette.setColor(palette.Background, QtGui.QColor(0, 170, 255))
        # "light" border
        palette.setColor(palette.Light, QtGui.QColor(255, 0, 0))
        # "dark" border
        palette.setColor(palette.Dark, QtGui.QColor(0, 255, 0))
        # set the palette
        lcd.setPalette(palette)
        lcd.display(value)

    def pop_dialog(self, params):
        self.dialog = PopUp(params)
        if self.dialog.exec_():
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
            # TODO: ComboBoxes are left, need to implement:
            # relay_combo = self.ui.relay_combo.currentText()
            self.ui.relay_combo.setCurrentIndex(parameters['relay_combo'])
            # el_combo = self.ui.electrode_combo.currentText()
            self.ui.electrode_combo.setCurrentIndex(parameters['el_combo'])
            print("done")
            self.startExp()
        # self.dialog.show()
        # # self.parameters = {''}
        # self.dialog.ui.buttonBox.accepted.connect(self.startExp)


class PopUp(QtWidgets.QDialog):
    def __init__(self, parameters):
        super(PopUp, self).__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.fillParams(parameters)

    def fillParams(self, params):
        self.ui.startV_box.setValue(float(params['startV']))
        self.ui.endV_box.setValue(float(params['endV']))
        self.ui.points_box.setValue(float(params['points']))
        self.ui.area_box.setValue(float(params['area']))
        self.ui.power_input_box.setValue(float(params['in_power']))
        self.ui.array_size_box.setValue(float(params['array_size']))
        self.ui.wait_box.setValue(float(params['wait']))
        self.ui.x_mean_box.setValue(float(params['x_mean']))
        # CheckBox: 0 - unchecked,  2- checked
        self.ui.fb_scan.setCheckState(params['fb_scan'])
        # TODO: ComboBoxes:
        self.ui.electrode_combo.setCurrentIndex(params['el_combo'])
        self.ui.relay_combo.setCurrentIndex(params['el_combo'])
        pass

    def GetAllParameters(self):
        startV = self.ui.startV_box.value()
        endV = self.ui.endV_box.value()
        points = self.ui.points_box.value()
        current_limit = self.ui.limitA_box.value()
        wait = self.ui.wait_box.value()
        array_size = self.ui.array_size_box.value()
        x_mean = self.ui.x_mean_box.value()
        el_area = self.ui.area_box.value()
        in_power = self.ui.power_input_box.value()
        fb_scan = self.ui.fb_scan.checkState()
        relay_combo = self.ui.relay_combo.currentIndex()
        el_combo = self.ui.electrode_combo.currentIndex()

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
                      'relay_combo':relay_combo,
                      'el_combo': el_combo}
        return parameters
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    # sys.argv always is equal at least to one, script itself.
    if len(sys.argv) > 1:
        if sys.argv[1] == "--fullscreen":
            window.showFullScreen()
        else:
            pass
    else:
        window.show()  # just show a window()
    sys.exit(app.exec_())

