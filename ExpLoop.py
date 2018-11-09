from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time


class LoopWorker(QObject):
    results = pyqtSignal(list, list, list, str, dict)
    errors = pyqtSignal(int, str)
    final = pyqtSignal(int)
    progress = pyqtSignal(str)

    def __init__(self, generator, oscilograph, *args, **kwargs):
        super(LoopWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self._require_stop = False
        self.Oscilograph.cmd_emiter.connect(self.emit_str)
        #
        self._measurement_parameters = {}
        self._current_ampl = 0
        self._current_offs = 0
        self._current_period = 0
        self._current_time_unit = ""
        # print("Init")
        pass