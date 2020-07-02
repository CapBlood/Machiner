"""Пользовательский графический интерфейс.

"""

import sys

from PySide2 import QtWidgets

from machiner.app.widgets.tab import TabBar
from machiner.app.widgets.tab_widget import ManagerWidget


class Window(QtWidgets.QTabWidget):
    """Класс окна.

    """

    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)
        self.setupUI()

    def setupUI(self):
        """Настройка интерфейса.

        """

        self.resize(800, 600)

        tabbar = TabBar(self)
        tabbar.setObjectName('tab')
        self.setObjectName('tab_widget')
        self.setTabBar(tabbar)
        self.setTabPosition(QtWidgets.QTabWidget.West)


def main():
    window = Window()
    manager = ManagerWidget()
    window.addTab(manager.buildSVM(), 'SVM')
    window.addTab(manager.buildTree(), 'Решающее дерево')
    return window


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open('design.qss').read())
    window = Window()
    manager = ManagerWidget()
    window.addTab(manager.buildSVM(), 'SVM')
    window.addTab(manager.buildTree(), 'Решающее дерево')
    window.show()
    sys.exit(app.exec_())
