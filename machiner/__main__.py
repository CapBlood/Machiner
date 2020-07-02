import os
import sys

from PySide2.QtWidgets import QApplication

from machiner.app.gui import main


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    appctxt = QApplication()
    appctxt.setStyle('Fusion')
    stylesheet = open(resource_path('design.qss'))
    appctxt.setStyleSheet(stylesheet.read())
    window = main()
    window.show()
    exit_code = appctxt.exec_()
    sys.exit(exit_code)
