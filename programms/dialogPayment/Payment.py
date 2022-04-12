from PyQt5 import uic
from PyQt5.QtWidgets import *
import sqlite3


class SetPayment(QDialog):
    def __init__(self, cabinet, time, date, button):
        QDialog.__init__(self)
        uic.loadUi('../programms/dialogPayment/PaymentWindow.ui', self)

        self.setWindowTitle('Оплата')

        self.cabinet = cabinet
        self.timer = time
        self.day = date
        self.btn = button

        self.db = sqlite3.connect('../data/seances.db')
        self.cursor = self.db.cursor()

        query = f''' SELECT attendance, cost, discount FROM seance 
        WHERE cabinet={self.cabinet} AND time="{self.timer}" AND day="{self.day}" '''
        texts = self.cursor.execute(query).fetchone()

        self.nallmoney.setText(texts[0].split(',')[0])
        self.cartmoney.setText(texts[0].split(',')[1])
        self.phonemoney.setText(texts[0].split(',')[2])
        self.predoplata.setText(texts[0].split(',')[3])

        self.predoplata.setReadOnly(True)

        self.cost = texts[1] - texts[2]

        if int(self.predoplata.text()) == self.cost:
            self.nallmoney.setReadOnly(True)
            self.cartmoney.setReadOnly(True)
            self.phonemoney.setReadOnly(True)

        self.btnBox.accepted.connect(self.acept_data)
        self.btnBox.rejected.connect(self.reject_data)

    def acept_data(self):
        pay = []
        if self.nallmoney.text() == '':
            pay.append('0')
        else:
            pay.append(self.nallmoney.text())
        if self.cartmoney.text() == '':
            pay.append('0')
        else:
            pay.append(self.cartmoney.text())
        if self.phonemoney.text() == '':
            pay.append('0')
        else:
            pay.append(self.phonemoney.text())
        if self.predoplata.text() == '':
            pay.append('0')
        else:
            pay.append(self.predoplata.text())
        query = f''' UPDATE seance SET attendance = "{','.join(pay)}"
        WHERE cabinet={self.cabinet} AND time="{self.timer}" AND day="{self.day}"'''
        self.cursor.execute(query)
        paying = list(map(int, pay))
        if sum(paying) == 0:
            self.btn.setStyleSheet('''
            background-color:rgb(225, 0, 0) ''')
        elif sum(paying) < self.cost:
            self.btn.setStyleSheet('''
            background-color:rgb(255, 223, 0) ''')
        else:
            self.btn.setStyleSheet('''
             background-color:rgb(0, 225, 0) ''')
        self.db.commit()
        self.db.close()
        self.close()

    def reject_data(self):
        self.close()
