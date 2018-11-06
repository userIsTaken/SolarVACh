from PyQt5 import QtWidgets, QtGui, QtCore
from Solar import Ui_MainWindow
from Dialog import Ui_SettingsDialog
import pyqtgraph
import sys
import numpy as np



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.jvView = self.ui.density_graph
        self.ui.pushButton.clicked.connect(self.hell)


    def hell(self):
        self.pop_dialog()
        self.draw_JV()
        self.draw_I()
        self.draw_P()
        self.updateQLCD()
        pass

    def updateQLCD(self):
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
        self.ui.lcdNumber.setPalette(palette)
        self.ui.lcdNumber.display(666)
        self.ui.lcdNumber_2.setPalette(palette)
        self.ui.lcdNumber_2.display(666)
        self.ui.lcdNumber_3.setPalette(palette)
        self.ui.lcdNumber_3.display(666)
        self.ui.lcdNumber_4.setPalette(palette)
        self.ui.lcdNumber_4.display(666)


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

        parameters = {'startV': startV,
                      'endV': endV,
                      'points': points,
                      'limitA': current_limit,
                      'wait': wait,
                      'array_size': array_size,
                      'x_mean': x_mean,
                      'area': el_area,
                      'in_power': in_power}
        return parameters
        pass

    def draw_JV(self):
        self.draw_method(self.ui.density_graph, 'Current density', 'A/cm^2', 'Voltage', 'V')
        pass

    def draw_I(self):
        self.draw_method(self.ui.current_graph, 'Current', 'A', 'Time', 's')
        pass

    def draw_P(self):
        self.draw_method(self.ui.power_graph, 'Power density', 'W/cm^2', 'Voltage', 'V')
        pass

    def draw_method(self, graph, x_title, x_scale, y_title, y_scale):
        x = np.random.normal(size=500)
        y = np.random.normal(size=500)
        graph.setBackground((255, 255, 255))
        graph.setLabel('bottom', x_title, x_scale)
        graph.setLabel('left', y_title, y_scale)
        graph.getAxis('bottom').setPen((0, 0, 0))
        graph.getAxis('left').setPen((0, 0, 0))
        graph.plot(x, y, pen=None, symbol='o')


    def pop_dialog(self):
        self.dialog = PopUp()
        self.dialog.show()


class PopUp(QtWidgets.QDialog):
    def __init__(self):
        super(PopUp, self).__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

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

