from PyQt5.QtWidgets import *
from AllConstants import *
from datetime import *
import sqlite3


class LastSeances(QWidget):
    def __init__(self, Pid):
        super().__init__()

        self.setGeometry(X_KORD, Y_KORD, 1000, 800)
        self.setWindowTitle(f'{CENTERNAME}: сеансы клиента')

        self.PersonsID = Pid

        self.allFrames = []

        self.combo = QComboBox(self)
        self.combo.resize(250, 30)
        self.combo.move(10, 10)

        self.scrollWidget = QScrollArea(self)
        self.scrollWidget.resize(980, 700)
        self.scrollWidget.move(10, 90)
        self.scrollWidget.show()

        self.db = sqlite3.connect('../data/seances.db')
        self.cursor = self.db.cursor()
        query = f''' SELECT seanceType FROM seance WHERE patient = "{self.PersonsID}" '''
        info = self.cursor.execute(query).fetchall()
        for i in info:
            self.combo.addItem(i[0])
        self.combo.addItem('Все')

    def DownloadInfo(self):
        layout = QGridLayout()

        query = f''' SELECT * FROM seance WHERE patient = "{self.PersonsID}" '''
        alldata = self.cursor.execute(query).fetchall()

        for _ in alldata:
            pass

        widget = QWidget()
        widget.setLayout(layout)
        self.scrollWidget.setWidget(widget)
