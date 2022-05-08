from PyQt5.QtWidgets import *
from AllConstants import *
from datetime import *
import sqlite3


class LastSeances(QWidget):
    def __init__(self, Pid):
        super().__init__()

        self.setGeometry(X_KORD, Y_KORD, 1200, 800)
        self.setFixedSize(1200, 800)
        self.setWindowTitle(f'{CENTERNAME}: сеансы клиента')

        self.PersonsID = Pid[0]

        self.allFrames = []

        self.combo = QComboBox(self)
        self.combo.resize(250, 30)
        self.combo.move(10, 10)
        self.combo.setFont(FONT)

        self.listwithseances = QListWidget(self)
        self.listwithseances.resize(1180, 740)
        self.listwithseances.move(10, 50)

        self.db = sqlite3.connect('../data/seances.db')
        self.cursor = self.db.cursor()
        query = f''' SELECT DISTINCT seanceType FROM seance WHERE patient = {self.PersonsID} '''
        info = self.cursor.execute(query).fetchall()
        self.combo.addItem('Все')
        for i in info:
            self.combo.addItem(i[0])

        self.combo.activated[str].connect(self.DownloadInfo)
        self.DownloadInfo('Все')

    def DownloadInfo(self, text):
        if text == 'Все':
            query = f''' SELECT day, time, cabinet, doctor, seanceType, cost
            FROM seance WHERE patient = {self.PersonsID} '''
        else:
            query = f''' SELECT day, time, cabinet, doctor, seanceType, cost
                        FROM seance WHERE patient = {self.PersonsID}
                         AND seanceType = "{text}" '''
        self.listwithseances.clear()
        alldata = self.cursor.execute(query).fetchall()
        alldata.sort()
        a = QListWidgetItem()
        a.setFont(FONT)
        line = ""
        line += "{:16}\tВремя:\tКабинет:\t{:25}\tСтоимость:\tТип сеанса:".format('Дата:', 'Доктор:')
        a.setText(line)
        self.listwithseances.addItem(a)
        for i in alldata:
            a = QListWidgetItem()
            a.setFont(FONT)
            line = ""
            day = i[0].split('-')
            day[1] = months[day[1]]
            line += '{:16}\t'.format(' '.join(reversed(day)))
            line += '{}\t'.format(i[1])
            line += '{}\t\t'.format(i[2])
            line += '{:25}\t'.format(' '.join(self.cursor.execute(f''' SELECT surname, name
             FROM doctors WHERE doctors_id = {i[3]}
             ''').fetchone()))
            line += '{}\t\t'.format(i[5])
            line += '{}'.format(i[4])
            a.setText(line)
            self.listwithseances.addItem(a)


