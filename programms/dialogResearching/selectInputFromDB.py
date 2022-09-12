from PyQt5 import uic
from PyQt5.QtWidgets import *
import sqlite3
from programms.AllConstants import *
from PyQt5.QtGui import QFont

FONT = QFont()
FONT.setPointSize(12)


def add_data_into_list(qlist, names):
    qlist.clear()

    for name in names:
        item = QListWidgetItem()
        if len(name) > 1:
            item.setText(' '.join(name[1:4]) + f' ID:{str(name[0])}')
        else:
            item.setText(str(name[0]))
        item.setFont(FONT)
        qlist.addItem(item)


class SelectInputData(QDialog):
    def __init__(self, table, ledit):
        QDialog.__init__(self)
        uic.loadUi('../programms/dialogResearching/diologWindow.ui', self)

        self.setWindowTitle('Диалоговое окно поиска')
        self.ledit = ledit

        self.table = table

        self.searchBarLedit.textChanged.connect(self.lineChanged)

        if table == 'seanceType':
            names = getInfoFromDB('DISTINCT seanceType', 'seance')
            names.sort()
        else:
            names = getInfoFromDB('*', table)
            names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
        add_data_into_list(self.AllData, names)

        self.returnData.accepted.connect(self.acept_data)
        self.returnData.rejected.connect(self.reject_data)

        self.currentLine = None
        self.AllData.clicked.connect(self.newSelectedLine)

    def acept_data(self):
        try:
            if self.table == 'seanceType':
                selected = self.AllData.currentItem().text()
            else:
                selected = self.AllData.currentItem().text()
            self.ledit.setText(selected)
        except AttributeError:
            pass
        self.close()

    def reject_data(self):
        self.close()

    def newSelectedLine(self):
        if not self.currentLine:
            self.currentLine = self.AllData.currentItem().text()
        elif self.currentLine == self.AllData.currentItem().text():
            self.acept_data()
        else:
            self.currentLine = self.AllData.currentItem().text()

    def lineChanged(self):
        text = self.searchBarLedit.text()
        if text.replace(' ', '') == '':
            if self.table == 'Patients' or self.table == 'Doctors':
                names = getInfoFromDB('*', '"' + self.table + '"')
                names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
            else:
                names = getInfoFromDB('DISTINCT seanceType', 'seance')
                names.sort()
            add_data_into_list(self.AllData, names)
        else:
            if self.table == 'Patients' or self.table == 'Doctors':
                surname = text.split(' ')
                names = self.getName(surname[0])
            else:
                names = getInfoFromDB('DISTINCT seanceType', 'seance', {'seanceType': [' LIKE ', '"%', text, '%"']})
                names.sort()
            add_data_into_list(self.AllData, names)

    def getName(self, surn):
        names = getInfoFromDB('*', '"' + self.table + '"', {'surname': [' LIKE ', '"%', surn.capitalize(), "%"],
                                                            'name': [' LIKE ', '"%', surn.capitalize(), "%"],
                                                            'patronymic': [' LIKE ', '"%', surn.capitalize(), "%"]},
                              'all', 'OR')
        names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
        return names
