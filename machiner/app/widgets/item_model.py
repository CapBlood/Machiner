"""Модуль моделей данных.

"""

from PySide2 import QtCore


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class ShareModel(QtCore.QAbstractTableModel):
    """Модель для хранения расшариваемых данных таблицы.

    Attributes:
        __data (list): данные в виде массива.

    """

    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__df = None
        self.__data = None

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Количество строк (items).

        """

        return len(self.__data) if self.__data is not None else 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        """Количество столбцов (items).

        """

        return len(self.__data[0]) if self.__data is not None else 0

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """Для расстановки хэдеров.

        Args:
            section (int): номер строки/столбца.
            orientation (int): ориентация обхода.
            role (int): роль выводимого элемента.

        """

        if (role == QtCore.Qt.DisplayRole
                and orientation == QtCore.Qt.Horizontal):
            return self.header_labels[section]
        return QtCore.QAbstractTableModel.headerData(self, section,
                                                     orientation, role)

    def loadData(self, df):
        """Загрузка Dataframe в таблицу.

        """

        self.header_labels = df.columns
        self.__df = df
        data = df.values.tolist()
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(), self.rowCount() + len(data) - 1)
        self.beginInsertColumns(QtCore.QModelIndex(),
                                self.columnCount(),
                                self.columnCount() + len(data[0]) - 1)
        self.__data = data
        self.endInsertColumns()
        self.endInsertRows()

    @property
    def headers(self):
        return self.header_labels if hasattr(self, 'header_labels') else None

    def removeColumn(self, header):
        """Удаление столбца.

        Args:
            header (str): название столбца для удаления.
        """

        begin_num = list(self.__df.columns).index(header)
        self.beginRemoveColumns(QtCore.QModelIndex(),
                                begin_num, begin_num)
        self.__df = self.__df.drop(columns=[header])
        self.header_labels = self.__df.columns
        self.__data = self.__df.values.tolist()
        self.endRemoveColumns()

    def clear(self):
        """Удаление всех данных.

        """

        self.beginResetModel()
        self.__data = None
        self.endResetModel()

    @property
    def array(self):
        """Получение данных таблицы.

        Returns:
            list: данные в виде таблицы.

        """

        return self.__data

    @property
    def dataframe(self):
        """Получение данных таблицы.

        Returns:
            Dataframe: данные в виде таблицы.

        """

        return self.__df

    def data(self, index, role):
        """Получение данных ячейки.

        Args:
            index (QModelIndex): индекс элемента.
            role (int): роль выводимого элемента.

        """

        if not index.isValid():
            return None

        if (index.row() >= len(self.__data)
                or index.column() >= len(self.__data[0])):
            return None

        # Для вывода в список.
        if role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()][index.column()]
        else:
            return None


class ParamItemModel(QtCore.QAbstractListModel):
    """Модель данных для хранения параметров методов
    машинного обучения.

    Args:
        kp (list): список кортежей вида
            (выводимое название, "истинное" название).
    """

    def __init__(self, kp, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__data = kp

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Количество строк (items).

        """

        return len(self.__data)

    def data(self, index, role):
        """Получение данных ячейки.

        Args:
            index (QModelIndex): индекс элемента.
            role (int): роль выводимого элемента.

        """

        if not index.isValid():
            return None

        if index.row() >= len(self.__data):
            return None

        # Для вывода в список.
        if role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()][0]
        # Для получение имени параметра.
        elif role == QtCore.Qt.UserRole:
            return self.__data[index.row()][1]
        else:
            return None

    def addParam(self, name, value):
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(), self.rowCount())
        self.__data.append((name, value))
        self.endInsertRows()


@singleton
class ShareComboModel(QtCore.QAbstractListModel):
    """Расшариваемый выпадающий список.

    """

    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        # Данные
        self.__data = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        """Количество строк (items).

        """

        return len(self.__data)

    def data(self, index, role):
        """Получение данных ячейки.

        Args:
            index (QModelIndex): индекс элемента.
            role (int): роль выводимого элемента.

        """

        if not index.isValid():
            return None

        if index.row() >= len(self.__data):
            return None

        # Для вывода в список.
        if role == QtCore.Qt.DisplayRole:
            return self.__data[index.row()]
        else:
            return None

    def clear(self):
        """Удаление всех данных.

        """

        self.beginResetModel()
        self.__data = []
        self.endResetModel()

    def addParams(self, values):
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(), self.rowCount())
        self.__data.extend(values)
        self.endInsertRows()
