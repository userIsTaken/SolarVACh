#!/usr/bin/python3
#-*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
from Solar_GUI import ApplicationWindow
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    # sys.argv always is equal at least to one, script itself.
    if len(sys.argv) > 1:
        if sys.argv[1] == "--fullscreen":
            window.showFullScreen()
        else:
            pass
        if sys.argv[1] == "-d" or sys.argv[1] == "--debug":
            print("DEBUG MODE")
            window.show()
            window.debug(True)
        else:
            pass
    else:
        window.show()  # just show a window()
    sys.exit(app.exec_())