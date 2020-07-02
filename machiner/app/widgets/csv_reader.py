"""Модуль виджета чтения csv."""

from PySide2 import QtWidgets
import pandas as pd

from machiner.app.widgets.item_model import ShareModel, ShareComboModel
from machiner.app.widgets.dialogs import ComboDialog


class CsvReader(QtWidgets.QWidget):
    """Класс виджета для чтения csv файла.

    Attributes:
        table (QTableWidget): таблица для отображения содержимого csv.

    """

    def __init__(self, parent=None):
        """Инициализатор.

        Args:
            parent (QWidget): виджет-родитель.

        """

        QtWidgets.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        """Настройка виджета."""

        vlayout = QtWidgets.QVBoxLayout()
        self.setLayout(vlayout)

        # Таблица для отображения данных.
        self.table = QtWidgets.QTableView()
        self.table.setModel(ShareModel())
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        vlayout.addWidget(self.table)

        # Кнопка для загрузки данных.
        button = QtWidgets.QPushButton('Загрузить CSV')
        button.clicked.connect(self.loadCsv)

        # Для параметров
        hlayout = QtWidgets.QHBoxLayout()
        vlayout.addLayout(hlayout)

        label = QtWidgets.QLabel('Целевой признак')
        hlayout.addWidget(label)

        self.combo = QtWidgets.QComboBox()
        self.combo.setModel(ShareComboModel())
        hlayout.addWidget(self.combo)

        # Кнопка для удаления столбца.
        button_del = QtWidgets.QPushButton('Удалить столбец')
        button_del.clicked.connect(self.removeColumn)

        # Область для дополнительных функциональных кнопок.
        hlayout = QtWidgets.QHBoxLayout()
        vlayout.addLayout(hlayout)
        hlayout.addWidget(button_del)

        # Область под таблицей для кнопки загрузки данных.
        hlayout = QtWidgets.QHBoxLayout()
        vlayout.addLayout(hlayout)
        hlayout.addWidget(button)

    def removeColumn(self):
        """Удаление столбца в таблице."""

        headers = self.table.model().headers
        if headers is None:
            QtWidgets.QMessageBox.critical(
                self, 'Ошибка', 'Сначала загрузите данные.')
            return

        header, ok = ComboDialog.getCombo(
            'Выберите необходимый столбец:', headers, parent=self)
        if not ok or header == '':
            return

        model_table = self.table.model()
        model_table.removeColumn(header)
        model_combo = self.combo.model()
        model_combo.clear()
        model_combo.addParams(model_table.dataframe.columns)

    def loadCsv(self):
        """Загрузка csv."""

        path, ok = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        if not ok or path == '':
            return

        df = pd.read_csv(path)

        model = self.combo.model()
        model.clear()
        model.addParams(df.columns)

        model = self.table.model()
        model.clear()
        model.loadData(df)
