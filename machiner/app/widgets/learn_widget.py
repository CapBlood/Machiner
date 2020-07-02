"""Модуль для виджета вывода информации о полученной модели ML.

"""


from PySide2 import QtWidgets


class LearnWidget(QtWidgets.QWidget):
    """Виджет для отображения результатов обучения модели ML.

    """

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setup()

    def setup(self):
        self.box = QtWidgets.QGridLayout()
        self.setLayout(self.box)

        self.box.addWidget(
            QtWidgets.QLabel('Accuracy (тестовая выборка):'), 0, 0)
        self.acc_test = QtWidgets.QLineEdit()
        self.acc_test.setReadOnly(True)
        self.box.addWidget(self.acc_test, 0, 1)

        self.box.addWidget(
            QtWidgets.QLabel('Accuracy (обучающая выборка):'), 1, 0)
        self.acc_train = QtWidgets.QLineEdit()
        self.acc_train.setReadOnly(True)
        self.box.addWidget(self.acc_train, 1, 1)

    def handleResult(self, params):
        """Получение результатов обучения модели ML.

        Args:
            params (dict): оценки модели ML.

        """

        self.acc_test.setText(str(params['accuracy_test']))
        self.acc_train.setText(str(params['accuracy_train']))
