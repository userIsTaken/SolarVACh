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
        self.parameters = {}
        self.current_arr = []
        self.voltage_arr = []

    #     Plots:
        self.density_graph = self.ui.density_graph.plot()
        self.current_graph = self.ui.current_graph.plot()

    def quit(self):
        try:
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
        except Exception as ex:
            print("ERR.CODE.A")
            print("wrong IP")
            print(str(ex))
        pass

    def hell(self):
        self.startExp()
        pass

    def startExp(self):
        self.parameters = {}
        self.parameters = self.GetAllParameters()
        self._thread = QThread()
        self._thread.setObjectName("WLoop")
        self._worker = LoopWorker(self.ExpensiveMeter, **self.parameters)
        self._worker.moveToThread(self._thread)
        self._worker.results.connect(self.draw_I)
        self._worker.current_results.connect(self.draw_graph)
        #self._worker.final.connect(self.WorkerEnded)
        #self._worker.errors.connect(self.ErrorHasBeenGot)
        #self._worker.progress.connect(self.ExperimentInfo)
        self._thread.started.connect(self._worker.run)
        self._thread.start()

        #self.draw_JV()
        #self.draw_I()
        #self.draw_P()
        #self.updateQLCD(self.ui.lcdNumber, 22.1)
        #self.updateQLCD(self.ui.lcdNumber_2, 85)
        #self.updateQLCD(self.ui.lcdNumber_3, 0.80)
        #self.updateQLCD(self.ui.lcdNumber_4, 29.5)
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
        relay_combo = self.ui.relay_combo.currentText()
        el_combo = self.ui.electrode_combo.currentText()


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

    def draw_graph(self, status, data_mean, err_rate, totalV, curr_array):
        self.ui.live_error.setText("error rate: ", err_rate)
        array = np.arange(0, self.parameters['array_size'], 1)
        self.draw_method(self.ui.current_graph, '6th dimension', 'a.u.', 'Current', 'A', array, curr_array)
        if status:
            self.current_arr.append(data_mean)
            self.voltage_arr.append(totalV)
            self.density_arr = [x / self.parameters['area'] for x in self.current_arr]
            self.draw_method(self.ui.density_graph, 'Voltage', 'V', 'Current', 'A', self.voltage_arr, self.current_arr)
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
        #y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        #x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
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

    def pop_dialog(self):
        self.dialog = PopUp(self.parameters)
        self.dialog.show()
        self.parameters = {''}
        self.dialog.ui.buttonBox.accepted.connect(self.startExp)


class PopUp(QtWidgets.QDialog):
    def __init__(self, parameters):
        super(PopUp, self).__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

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
        relay_combo = self.ui.relay_combo.currentText()
        el_combo = self.ui.electrode_combo.currentText()

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

