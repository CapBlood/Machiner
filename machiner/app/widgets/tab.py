"""Модуль виджета вкладок для QTabWidget.

"""


from PySide2 import QtGui, QtCore, QtWidgets


class TabBar(QtWidgets.QTabBar):
    """Класс вкладок для QTabWidget.

    """

    def tabSizeHint(self, index):
        """Размер для вкладок.

        Returns:
            QRect: размер вкладки.

        """

        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        s.setHeight(s.height() * 3)
        s.setWidth(s.width() * 0.7)
        return s

    def paintEvent(self, event):
        """Отрисовка вкладок и заголовков в них.

        """

        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            if not event.region().contains(self.tabRect(i)):
                continue

            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i)
            text = self.tabText(i)
            painter.drawText(c, QtCore.Qt.AlignCenter | QtCore.Qt.TextWordWrap,
                             text)
            painter.restore()
