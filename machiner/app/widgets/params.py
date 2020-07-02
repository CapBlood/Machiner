"""Виджет для задания параметров модели машинного обучения."""


from PySide2 import QtWidgets, QtCore
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from machiner.app.widgets.item_model import ParamItemModel, ShareModel


class BuilderParam():
    """Конструктор виджета параметров."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.__widget = ParamWidget()

    def widget(self):
        widget = self.__widget
        self.reset()
        return widget

    def setModel(self, model):
        """Настройка модели машинного обучения."""

        self.__widget.cls_model = model

    def addComboParam(self, text, name, params):
        """Добавление выпадающего списка параметра.

        Args:
            text (str): отображаемый текст-описание параметра.
            name (str): название параметра.
            params (list): список кортежей вида пары (отображаемое значение,
                значение параметра).
        """

        row = self.__widget.layout.rowCount()

        label = QtWidgets.QLabel(text)
        self.__widget.layout.addWidget(label, row,
                                       0)

        combo = QtWidgets.QComboBox()
        combo.setModel(ParamItemModel(params))
        self.__widget.layout.addWidget(combo, row,
                                       1)

        self.__widget.combos.append({'name': name, 'widget': combo})

    def addLineParam(self, text, name, default_value):
        """Добавление строки ввода параметра.

        Args:
            text (str): отображаемый текст-описание параметра.
            name (str): название параметра.
            default_value (str): значение параметра по умолчанию.
        """

        row = self.__widget.layout.rowCount()

        label = QtWidgets.QLabel(text)
        self.__widget.layout.addWidget(label, row,
                                       0)

        line = QtWidgets.QLineEdit(default_value)
        self.__widget.layout.addWidget(line, row,
                                       1)

        self.__widget.lines.append({'name': name, 'widget': line})


class ParamWidget(QtWidgets.QWidget):
    """Виджет для ввода параметров модели ML."""

    # Сигнал для отправки результатов обучения модели.
    sendResult = QtCore.Signal(dict)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)

        self.combos = []
        self.lines = []
        self.target = None
        self.cls_model = None
        self.model = None

        self.setup()

    def setup(self):
        """Для настройки виджета."""

        vbox = QtWidgets.QVBoxLayout()
        self.setLayout(vbox)

        # Область для виджетов настройки параметров.
        self.layout = QtWidgets.QGridLayout()
        vbox.addLayout(self.layout)

        vbox.addStretch(5)

        # Кнопка для обучения
        hbox = QtWidgets.QHBoxLayout()
        button = QtWidgets.QPushButton('Обучить')
        hbox.addWidget(button)
        vbox.addLayout(hbox)

        button.clicked.connect(self.train)

    def getParamsByLines(self):
        """Получение параметров из строк ввода."""

        params = {}
        for line in self.lines:
            text = line['widget'].text()
            f = float(text)
            i = int(f)
            value = i if i == f else f
            params[line['name']] = value
        return params

    def getParamsByCombos(self):
        """Получение параметров из выпадающих списков."""

        params = {}
        for combo in self.combos:
            params[combo['name']] = combo['widget'].itemData(
                combo['widget'].currentIndex())
        return params

    def getParams(self):
        """Получение всех параметров."""

        try:
            params = dict(self.getParamsByCombos(), **self.getParamsByLines())
        except ValueError:
            params = None
        return params

    def handleTarget(self, target):
        """Получение имени целевого признака.

        Args:
            target (str): название целевого признака.
        """

        self.target = target

    def train(self):
        """Обучение модели ML."""

        data = ShareModel().dataframe
        if data is None:
            QtWidgets.QMessageBox.critical(
                self, 'Ошибка', 'Не загружены данные для обучения.')
            return

        if self.target is None:
            QtWidgets.QMessageBox.critical(
                self, 'Ошибка', 'Не задан целевой признак.')
            return

        # Создание модели с заданными параметрами.

        params = self.getParams()
        if params is None:
            QtWidgets.QMessageBox.critical(
                self, 'Ошибка', 'Некорректные параметры.')
            return

        self.model = self.cls_model(**params)

        X, y = data.drop(columns=[self.target]), data[self.target]

        if X.empty or y.empty:
            QtWidgets.QMessageBox.critical(
                self, 'Ошибка', 'Отсутствуют данные для обучения.')
            return

        train_X, test_X, train_y, test_y = train_test_split(X, y,
                                                            test_size=0.3)

        try:
            # Обучение.
            self.model.fit(train_X, train_y)
        except ValueError as e:
            QtWidgets.QMessageBox.critical(
                self, 'Ошибка', str(e))
            return

        # Ошибка на тесте.
        y_pred = self.model.predict(test_X)
        score_test = accuracy_score(y_pred, test_y)
        # Ошибка на обучении.
        y_pred = self.model.predict(train_X)
        score_train = accuracy_score(y_pred, train_y)

        data = {'accuracy_test': score_test, 'accuracy_train': score_train}

        # Передача результата в виджет отображение результатов обучения.
        self.sendResult.emit(data)


class ManagerParam():
    # Параметры метода опорных векторов.
    svm_params = {
        'kernel': [('Linear', 'linear'),
                   ('Polynomial', 'poly'),
                   ('RBF', 'rbf'),
                   ('Sigmoid', 'sigmoid')],
        'degree': '3',
        'C': '1.0'
    }
    # Параметры решающего дерева.
    tree_params = {
        'criterion': [('Gini', 'gini'),
                      ('Entropy', 'entropy')],
        'max_depth': '',
        'min_samples_split': '2'
    }

    def __init__(self):
        self.__builder = BuilderParam()

    def buildSVM(self):
        self.__builder.addComboParam('Ядро', 'kernel',
                                     self.svm_params['kernel'])
        self.__builder.addLineParam(
            'Степень полинома (только для полиномиального ядра)',
            'degree', self.svm_params['degree'])
        self.__builder.addLineParam(
            'Параметр регуляризации',
            'C', self.svm_params['C'])
        self.__builder.setModel(SVC)
        return self.__builder.widget()

    def buildTree(self):
        self.__builder.addComboParam('Критерий прироста информации',
                                     'criterion',
                                     self.tree_params['criterion'])
        self.__builder.addLineParam('Максимальная глубина дерева', 'max_depth',
                                    self.tree_params['max_depth'])
        self.__builder.addLineParam(
            'Минимальное количество сэмплов для разбиения',
            'min_samples_split',
            self.tree_params['min_samples_split'])
        self.__builder.setModel(DecisionTreeClassifier)
        return self.__builder.widget()
