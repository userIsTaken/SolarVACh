from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject
import os, sys
import time


class LoopWorker(QObject):
    results = pyqtSignal()
    errors = pyqtSignal(int, str)
    final = pyqtSignal(int)
    progress = pyqtSignal(str)

    def __init__(self, meter, *args, **kwargs):
        super(LoopWorker, self).__init__()
        self.args = args
        self.params = kwargs
        self.ExpensiveMeter = meter
        self._require_stop = False
        self._measurement_parameters = {}
        pass

    @pyqtSlot()
    def run(self):
        try:
            #startV = self.params['startV']
            #endV = self.params['endV']
            self.results.emit()
        except:
            print('blah')
    pass
