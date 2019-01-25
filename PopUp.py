from PyQt5 import QtWidgets, QtGui
from GUI.Dialog import Ui_SettingsDialog


class PopUp(QtWidgets.QDialog):
    def __init__(self, parameters):
        super(PopUp, self).__init__()
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.fillParams(parameters)
        self.ui.relay_combo.currentIndexChanged.connect(self.comboUpdate)

    def comboUpdate(self):
        """
                index is from zero
                :return:
                """
        i = self.ui.relay_combo.currentIndex()
        self.ui.electrode_combo.setCurrentIndex(6 - (i + 1))


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
        self.ui.sc_name.setPlainText(params['sc_name'])
        self.setMode(params['mode'])
        self.ui.timeDelayBox.setValue(params['delay_min'])
        self.ui.countBox.setValue(params['counts'])
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
        pass

    def getMode(self):
        """

        :return: one contact mode 0, time mode 1, relay mode 2
        """
        mode = 0  # default 0, time mode 1, relay mode 2
        if self.ui.timeMode.isChecked():
            mode = 1
        elif self.ui.relayMode.isChecked():
            mode = 2
        elif self.ui.oneShotMode.isChecked():
            mode = 0
        else:
            mode = 0
        return mode
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
        sc_name = self.ui.sc_name.toPlainText()
        mode = self.getMode()
        delay_min = self.ui.timeDelayBox.value()
        counts = self.ui.countBox.value()
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
                      'el_combo': el_combo,
                      'sc_name':sc_name,
                      'mode':mode,
                      'delay_min':delay_min,
                      'counts':counts}
        return parameters
        pass