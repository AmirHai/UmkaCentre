from PyQt5 import uic
from datetime import date
from PyQt5.QtWidgets import *


class CalendarDialog(QDialog):
    def __init__(self, newData):
        QDialog.__init__(self)
        uic.loadUi('../programms/dialogCalendary/CalendarDialog.ui', self)

        self.setWindowTitle('выберите дату:')

        self.changedDate.setReadOnly(True)

        self.newdata = newData

        self.Boxbtn.accepted.connect(self.acept_data)
        self.Boxbtn.rejected.connect(self.reject_data)
        self.Boxbtn.clicked.connect(self.reset_data)
        self.calendar.clicked.connect(self.change)

    def change(self):
        data = date(*[int(i) for i in self.calendar.selectedDate().toString('yyyy MM dd').split(' ')])
        self.changedDate.setText(data.strftime('%d %B %Y'))

    def acept_data(self):
        self.newdata.setText(self.changedDate.text())
        self.close()

    def reject_data(self):
        self.close()

    def reset_data(self):
        self.newdata.setText(date.today().strftime('%d %B %Y'))
        self.close()