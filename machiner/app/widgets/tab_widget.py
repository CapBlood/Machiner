"""Модуль виджета содержимого вкладок методов машинного обучения.

"""

from PySide2 import QtWidgets

from machiner.app.widgets.csv_reader import CsvReader
from machiner.app.widgets.params import ManagerParam
from machiner.app.widgets.learn_widget import LearnWidget


class BuilderTab():
    """Конструктор виджета для вкладок методов машинного обучения.

    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.__widget = MainWidget()

    def widget(self):
        widget = self.__widget
        self.reset()
        return widget

    def addModel(self, wparam, wlearn):
        """Добавление виджетов для инициализации модели
        машинного обучения.

        Args:
            wparam (QWidget): виджет для отображения параметров модели
                машинного обучения.
            wlearn (QWidget): виджет для отображения результатов обучения
                модели машинного обучения.
        """

        csv_reader = CsvReader()
        csv_reader.combo.currentTextChanged.connect(wparam.handleTarget)
        wparam.sendResult.connect(wlearn.handleResult)
        self.__widget.tab.addTab(csv_reader, 'Данные')
        self.__widget.tab.addTab(wparam, 'Параметры')
        self.__widget.tab.addTab(wlearn, 'Обучение')


class MainWidget(QtWidgets.QWidget):
    """Класс виджета для отображения содержимого вкладки методов
    машинного обучения.

    """

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(vlayout)

        self.tab = QtWidgets.QTabWidget()
        self.tab.setObjectName('menu')
        self.tab.tabBar().setObjectName('menu_bar')
        vlayout.addWidget(self.tab)


class ManagerWidget():
    """Менеджер сборки виджетов для различных вкладок методов
    машинного обучения.

    """

    def __init__(self):
        self.__builder = BuilderTab()
        self.__manager_param = ManagerParam()

    def buildSVM(self):
        self.__builder.addModel(self.__manager_param.buildSVM(),
                                LearnWidget())
        return self.__builder.widget()

    def buildTree(self):
        self.__builder.addModel(self.__manager_param.buildTree(),
                                LearnWidget())
        return self.__builder.widget()
