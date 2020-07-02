"""Модуля для диалоговых окон."""


from PySide2 import QtWidgets, QtCore


class ComboDialog(QtWidgets.QDialog):
    """Диалоговое окно с выпадающим списком.

    Args:
        l_combo (list): список строк - вариантов выбора.
    """

    def __init__(self, text, l_combo, parent=None):
        QtWidgets.QDialog.__init__(self, parent=parent)
        self.setup(text, l_combo)

    def setup(self, text, l_combo):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.label = QtWidgets.QLabel(text)
        layout.addWidget(self.label)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(l_combo)
        layout.addWidget(self.combo)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def choice(self):
        return self.combo.currentText()

    @staticmethod
    def getCombo(text, l_combo, parent=None):
        """Вызов окна с выпадающим списком.

        Args:
            l_combo (list): список строк - вариантов выбора.
        """

        dialog = ComboDialog(text, l_combo, parent=parent)
        result = dialog.exec_()
        choice = dialog.choice()
        return choice, result == QtWidgets.QDialog.Accepted
