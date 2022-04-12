from personCard import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QFont
from AllConstants import *
import sqlite3


class Patients(QWidget):
    def __init__(self, table, returning=False):
        super().__init__()

        uic.loadUi('../activities/researchPerson.ui', self)
        self.setGeometry(X_KORD, Y_KORD, WINDOWWIDTH, WINDOWHEIGHT)
        self.setFixedSize(600, 800)
        if table == 'patients':
            self.setWindowTitle(f'{CENTERNAME}: пациенты')
        elif table == 'doctors':
            self.setWindowTitle(f'{CENTERNAME}: доктора')

        self.table = table
        self.retur = returning
        self.allButtons = []

        self.db = sqlite3.connect('../data/seances.db')
        self.cursor = self.db.cursor()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.resize(580, 740)
        self.scrollArea.move(10, 50)
        self.scrollArea.show()

        self.files = []

        self.searchBarLedit.textChanged.connect(self.lineChanged)

        query = f''' SELECT * FROM "{self.table}" '''
        names = self.cursor.execute(query).fetchall()
        names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))

        self.takeAllData(names)
        self.addbtn.clicked.connect(self.addPerson)

    def takeAllData(self, names):
        layout = QVBoxLayout()
        n = '-' * 78
        lbl = QLabel(n)
        lbl.setFont(FONT)
        lbl.setStyleSheet("text-align: left")
        layout.addWidget(lbl)
        self.allButtons.clear()

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
                query = f''' SELECT * FROM "{self.table}" '''
                names = self.cursor.execute(query).fetchall()
                names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
            else:
                query = f''' SELECT DISTINCT seanceType FROM seanse '''
                names = self.cursor.execute(query).fetchall()
                names.sort()
            self.takeAllData(names)
        else:
            if self.table == 'patients' or self.table == 'doctors':
                surname = text.split(' ')
                names = self.getName(surname[0])
            else:
                query = f''' SELECT DISTINCT seanceType FROM seanse WHERE seanceType LIKE "%{text}%" '''
                names = self.cursor.execute(query).fetchall()
                names.sort()
            self.takeAllData(names)

    def getName(self, surn):
        query = f''' SELECT * FROM "{self.table}" WHERE 
        surname LIKE "%{surn.capitalize()}%" OR name LIKE "%{surn.capitalize()}%"
         OR patronymic LIKE "%{surn.capitalize()}%" '''
        names = self.cursor.execute(query).fetchall()
        names.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
        return names

    def btnClicked(self):
        send = self.sender().text().split(' ')
        if self.table == 'patients':
            query = f''' SELECT patients_id FROM patients
                WHERE "{send[0]}" = surname AND "{send[1]}" = name AND "{send[2]}" = patronymic '''
            id = self.cursor.execute(query).fetchall()
            self.card = PersonCard(id[0])
        else:
            query = f''' SELECT doctors_id FROM doctors
                 WHERE "{send[0]}" = surname AND "{send[1]}" = name AND "{send[2]}" = patronymic '''
            id = self.cursor.execute(query).fetchall()
            self.card = DoctorsCard(id[0])
        self.card.show()

    def addPerson(self):
        if self.table == 'patients':
            name, ok = QInputDialog.getText(self, 'добавление пациента', 'введите ФИО')
        else:
            name, ok = QInputDialog.getText(self, 'добавление доктора', 'введите ФИО')
        print(name)
        if len(name.split(' ')) != 3:
            QMessageBox.critical(self, " Ошибка! ", " неправильный ввод данных!!! ", QMessageBox.Ok)
        else:
            names = name.split(' ')
            if self.table == 'patients':
                neededID = len(self.cursor.execute(''' SELECT * FROM patients ''').fetchall()) + 1
                query = f""" INSERT INTO patients 
                    VALUES ({neededID}, '{names[0].capitalize()}', '{names[1].capitalize()}',
                    '{names[2].capitalize()}', 0); """
                self.cursor.execute(query)
                self.db.commit()
                file = open(f'../data/patients/ID{neededID}.txt', 'w+', encoding='utf-8')
                file.write(' '.join([i.capitalize() for i in names]))
                file.close()
            else:
                neededID = len(self.cursor.execute(''' SELECT * FROM doctors ''').fetchall()) + 1
                query = f""" INSERT INTO doctors 
                VALUES ({neededID}, '{names[0].capitalize()}', '{names[1].capitalize()}',
                 '{names[2].capitalize()}'); """
                self.cursor.execute(query)
                self.db.commit()
                file = open(f'../data/doctors/ID{neededID}.txt', 'w+', encoding='utf-8')
                file.write(' '.join([i.capitalize() for i in names]))
                file.close()

        query = f''' SELECT * FROM "{self.table}" '''
        n = self.cursor.execute(query).fetchall()

        n.sort(key=lambda x: (x[1], x[2], x[3], x[0]))
        self.takeAllData(n)
