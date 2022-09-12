from personCard import *
from PyQt5 import uic
from AllConstants import *
import sqlite3


class Patients(QWidget):
    def __init__(self, table, grid=None, returning=False):
        super().__init__()

        uic.loadUi('../activities/researchPerson.ui', self)
        self.setGeometry(X_KORD, Y_KORD, WINDOWWIDTH, WINDOWHEIGHT)
        self.setFixedSize(950, 950)
        if table == 'patients':
            self.setWindowTitle(f'{CENTERNAME}: пациенты')
        elif table == 'doctors':
            self.setWindowTitle(f'{CENTERNAME}: доктора')

        self.table = table
        self.retur = returning
        self.allButtons = []
        self.GridLayout = grid

        self.scrollArea = QScrollArea(self)
        self.scrollArea.resize(940, 900)
        self.scrollArea.move(10, 50)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.show()

        self.files = []

        self.searchBarLedit.textChanged.connect(self.lineChanged)
        names = getInfoFromDB('*', '"' + self.table + '"')
        names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))

        self.takeAllData(names)
        self.addbtn.clicked.connect(self.addPerson)

    def takeAllData(self, names):
        layout = QVBoxLayout()
        self.allButtons.clear()

        if len(names) < 18:
            self.scrollArea.resize(940, 50 * len(names))
        else:
            self.scrollArea.resize(940, 900)

        for i in names:
            if self.table == 'patients' or self.table == 'doctors':
                n = ' '.join([str(j) for j in i[1:4]]) + ' ' * 20
            else:
                n = ' '.join([str(j) for j in i]) + ' ' * 50
            self.allButtons.append(QPushButton(n))
            self.allButtons[-1].setFont(FONT)
            self.allButtons[-1].setStyleSheet("text-align: left")
            self.allButtons[-1].clicked.connect(self.btnClicked)
            layout.addWidget(self.allButtons[-1])

        widget = QWidget()
        widget.setLayout(layout)
        self.scrollArea.setWidget(widget)

    def lineChanged(self):
        text = self.searchBarLedit.text()
        if text.replace(' ', '') == '':
            if self.table == 'patients' or self.table == 'doctors':
                names = getInfoFromDB('*', '"' + self.table + '"')
                names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
            else:
                names = getInfoFromDB('DISTINCT seanceType', 'seance')
                names.sort()
            self.takeAllData(names)
        else:
            if self.table == 'patients' or self.table == 'doctors':
                surname = text.split(' ')
                names = self.getName(surname[0])
            else:
                names = getInfoFromDB('DISTINCT seanceType', 'seance', {'seanceType': [' LIKE ', '"%', text, '%"']})
                names.sort()
            self.takeAllData(names)

    def getName(self, surn):
        names = getInfoFromDB('*', f"{self.table}", {'surname': [' LIKE ', '"%', surn.capitalize(), '%"'],
                                                     'name': [' LIKE ', '"%', surn.capitalize(), '%"'],
                                                     'patronymic': [' LIKE ', '"%', surn.capitalize(), '%"']},
                              'all', 'OR')
        names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
        return names

    def btnClicked(self):
        send = self.sender().text().split(' ')
        if self.table == 'patients':
            id = getInfoFromDB('patients_id', 'patients', {'surname': ['=', '"', send[0], '"'],
                                                           'name': ['=', '"', send[1], '"'],
                                                           'patronymic': ['=', '"', send[2], '"']})
            self.card = PersonCard(id[0])
        else:
            id = getInfoFromDB('doctors_id', 'doctors', {'surname': ['=', '"', send[0], '"'],
                                                         'name': ['=', '"', send[1], '"'],
                                                         'patronymic': ['=', '"', send[2], '"']})
            self.card = DoctorsCard(id[0])
        if not self.GridLayout:
            self.card.show()
        else:
            self.GridLayout.addWidget(self.card, 0, 1)

    def addPerson(self):
        if self.table == 'patients':
            name, ok = QInputDialog.getText(self, 'добавление пациента', 'введите ФИО')
        else:
            name, ok = QInputDialog.getText(self, 'добавление доктора', 'введите ФИО')
        if len(name.split(' ')) != 3:
            QMessageBox.critical(self, " Ошибка! ", " неправильный ввод данных!!! ", QMessageBox.Ok)
        else:
            names = name.split(' ')
            if self.table == 'patients':
                neededID = len(getInfoFromDB('*', 'patients')) + 1
                addInfoFromDB('patients', ['patients_id', 'surname', 'name', 'patronymic', 'money'],
                              [neededID, f'{names[0].capitalize()}', f'{names[1].capitalize()}',
                               f'{names[2].capitalize()}', 0])

                file = open(f'../data/patients/ID{neededID}.txt', 'w+', encoding='utf-8')
                file.write(' '.join([i.capitalize() for i in names]))
                file.close()
            else:
                neededID = len(getInfoFromDB('*', 'doctors')) + 1
                addInfoFromDB('doctors', ['doctors_id', 'surname', 'name', 'patronymic'],
                              [neededID, f'{names[0].capitalize()}', f'{names[1].capitalize()}',
                               f'{names[2].capitalize()}'])
                file = open(f'../data/doctors/ID{neededID}.txt', 'w+', encoding='utf-8')
                file.write(' '.join([i.capitalize() for i in names]))
                file.close()

        n = getInfoFromDB('*', f"{self.table}")

        n.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
        self.takeAllData(n)
