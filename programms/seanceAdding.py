from AllConstants import *
from dialogResearching import selectInputFromDB
from PyQt5 import uic
import datetime
from dialogPayment import Payment


class CreateSeance(QWidget):
    def __init__(self, changing=False, *args):
        super().__init__()

        self.setGeometry(X_KORD, Y_KORD, 800, 700)
        self.setFixedSize(800, 700)
        uic.loadUi('../activities/addSeance.ui', self)

        self.db = sqlite3.connect('../data/seances.db')
        self.cursor = self.db.cursor()

        self.curDate = self.date.selectedDate().toString('yyyy-MM-dd')
        self.date.clicked.connect(self.calendarChanged)

        self.AllDates = []

        self.ledit_doctors.setReadOnly(True)
        self.ledit_patients.setReadOnly(True)

        self.timedelta.addItems(CONST.keys())

        self.doc_id = 0
        self.pat_id = 0

        self.changing = changing

        if self.changing:
            self.changingInfo = args[0]
            self.ChangeSeanceTrue()

        self.Doctors.clicked.connect(self.researching)
        self.Patients.clicked.connect(self.researching)
        self.seanceType.clicked.connect(self.researching)
        self.btn_add.clicked.connect(self.addSeancePressed)
        self.btn_Payment.clicked.connect(self.paymentClicked)

    def researching(self):
        if self.sender().objectName() == 'Doctors':
            data = selectInputFromDB.SelectInputData(self.sender().objectName(), self.ledit_doctors)
            data.show()
            data.exec_()
            try:
                self.doc_id = self.ledit_doctors.text().split(':')[1]
            except IndexError:
                pass
        elif self.sender().objectName() == 'Patients':
            data = selectInputFromDB.SelectInputData(self.sender().objectName(), self.ledit_patients)
            data.show()
            data.exec_()
            try:
                self.pat_id = self.ledit_patients.text().split(':')[1]
            except IndexError:
                pass
        else:
            data = selectInputFromDB.SelectInputData(self.sender().objectName(), self.ledit_seance)
            data.show()
            data.exec_()

    def addSeancePressed(self):
        if not self.changing:
            Id = self.cursor.execute(''' SELECT seance_id FROM seance ''').fetchall()
            Id.sort()
            if len(Id):
                Id = Id[-1][0] + 1
            else:
                Id = 1
            time = self.time.time().toString('HH:mm')
            if self.present.text() == '':
                present = 0
            else:
                present = int(self.present.text())
            if self.doc_id and self.pat_id and self.ledit_seance.text() and self.cabinet.text() and self.cost.text():
                for obj, i in enumerate(self.AllDates):
                    attendance = self.MoneyExamination()
                    query = f''' INSERT INTO seance (seance_id, day, time, cabinet, 
                    doctor, patient, seanceType, cost, attendance, discount, deltatime)
                    VALUES ({Id + obj}, "{i}", "{time}", {int(self.cabinet.text())}, {self.doc_id}, {self.pat_id},
                    "{self.ledit_seance.text()}", {int(self.cost.text())}, "{attendance}",
                    {present}, {CONST[self.timedelta.currentText()]}); '''
                    self.cursor.execute(query)
                    self.db.commit()
                self.db.close()
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка", "Данные введены неправильно", QMessageBox.Ok)
        else:
            if self.doc_id and self.ledit_seance.text() and self.cabinet.text() and self.cost.text():
                attendance = self.costChanged()
                self.cursor.execute(f'''
        UPDATE seance SET day="{self.date.selectedDate().toString('yyyy-MM-dd')}",
     time="{self.time.time().toString('HH:mm')}", cabinet={int(self.cabinet.text())},
     doctor={self.doc_id}, seanceType="{self.ledit_seance.text()}", cost={int(self.cost.text())},
     discount={int(self.present.text())}, deltatime={CONST[self.timedelta.currentText()]},
      attendance="{','.join([str(i) for i in attendance])}"
        WHERE seance_id={self.seanceId}''')
                self.db.commit()
                self.db.close()
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка", "Данные введены неправильно", QMessageBox.Ok)

    def MoneyExamination(self):
        present = 0
        if self.present.text():
            present = int(self.present.text())
        moneyInProfile = self.cursor.execute(f'''
                        SELECT money FROM patients WHERE patients_id={self.pat_id}
                        ''').fetchone()[0]
        if moneyInProfile >= int(self.cost.text()) - present:
            moneyInProfile -= int(self.cost.text())
            query = f''' UPDATE patients SET money = {moneyInProfile} WHERE patients_id={self.pat_id}'''
            self.cursor.execute(query)
            self.db.commit()
            return f"0,0,0,{int(self.cost.text()) - present}"
        elif moneyInProfile > 0:
            query = f''' UPDATE patients SET money = {0} WHERE patients_id={self.pat_id}'''
            self.cursor.execute(query)
            self.db.commit()
            return f'0,0,0,{moneyInProfile}'
        elif moneyInProfile == 0:
            return f'0,0,0,0'

    def costChanged(self):
        attendance = sum([int(i) for i in self.cursor.execute(f''' 
        SELECT attendance FROM seance WHERE seance_id={self.seanceId} ''').fetchone()[0].split(',')])
        newAttendance = [0, 0, 0, attendance]
        newCost = int(self.cost.text())
        moneySum = self.cursor.execute(f'''
                SELECT money FROM patients WHERE patients_id={self.pat_id}''').fetchone()[0]
        addMoney = 0
        if self.lastCost != newCost:
            self.changingInfo[-1].setText(str(newCost))
            if self.lastCost == attendance:
                if self.lastCost > newCost:
                    newAttendance[3] -= self.lastCost - newCost
                    addMoney += self.lastCost - newCost
                else:
                    if moneySum >= newCost - self.lastCost:
                        newAttendance[-1] = newCost
                        moneySum -= newCost - self.lastCost
                        self.changingInfo[-1].setStyleSheet('''
                        background-color:rgb(0, 225, 0) ''')
                    else:
                        newAttendance[-1] += moneySum
                        moneySum = 0
                        self.changingInfo[-1].setStyleSheet('''
                        background-color:rgb(255, 223, 0) ''')
            elif attendance > 0:
                if self.lastCost > newCost:
                    if attendance > newCost:
                        newAttendance[3] = newCost
                        addMoney += attendance - newCost
                        self.changingInfo[-1].setStyleSheet('''
                                background-color:rgb(0, 225, 0) ''')
                    elif 0 < attendance < newCost:
                        if moneySum < newCost - attendance:
                            newAttendance[-1] += moneySum
                            moneySum = 0
                            self.changingInfo[-1].setStyleSheet('''
                            background-color:rgb(255, 223, 0) ''')
                        else:
                            newAttendance[-1] = newCost
                            moneySum -= newCost - attendance
                            self.changingInfo[-1].setStyleSheet('''
                            background-color:rgb(0, 225, 0) ''')
            else:
                if moneySum >= newCost:
                    moneySum -= newCost
                    newAttendance[-1] = newCost
                    self.changingInfo[-1].setStyleSheet('''
                    background-color:rgb(0, 225, 0) ''')
                elif moneySum > 0:
                    newAttendance = moneySum
                    moneySum = 0
                    self.changingInfo[-1].setStyleSheet('''
                    background-color:rgb(255, 223, 0) ''')
                else:
                    self.changingInfo[-1].setStyleSheet('''
                    background-color:rgb(225, 0, 0) ''')
        else:
            newAttendance = [int(i) for i in self.allInfo[8].split(',')]
            if attendance < newCost:
                if moneySum >= newCost - attendance:
                    moneySum -= newCost - attendance
                    newAttendance[-1] += newCost - attendance
                else:
                    newAttendance[-1] += moneySum
                    moneySum = 0
        moneySum += addMoney
        self.cursor.execute(f''' UPDATE patients SET money={moneySum} WHERE patients_id={self.pat_id} ''')
        return newAttendance

    def calendarChanged(self):
        if self.date.selectedDate().toString('yyyy-MM-dd') == self.curDate:
            if self.curDate not in self.AllDates:
                self.AllDates.append(self.curDate)
                self.AllDates.sort()
            else:
                self.AllDates.remove(self.curDate)
        else:
            self.curDate = self.date.selectedDate().toString('yyyy-MM-dd')
        self.selectDates.clear()
        for i in self.AllDates:
            a = QListWidgetItem()
            a.setFont(FONT)
            text = i.split('-')
            text[1] = months[text[1]]
            a.setText(' '.join(reversed(text)))
            self.selectDates.addItem(a)

    def ChangeSeanceTrue(self):
        self.btn_add.setText('Изменить')
        self.allInfo = self.cursor.execute(f'''
        SELECT * FROM seance WHERE cabinet={self.changingInfo[0]} AND time="{self.changingInfo[1]}"
        AND day="{self.changingInfo[2]}"
        ''').fetchone()
        self.ledit_doctors.setText(' '.join(self.cursor.execute(f'''
        SELECT surname, name, patronymic FROM doctors WHERE doctors_id={self.allInfo[4]}
        ''').fetchone()))
        self.ledit_patients.setText(' '.join(self.cursor.execute(f'''
        SELECT surname, name, patronymic FROM patients WHERE patients_id={self.allInfo[5]}
        ''').fetchone()))
        self.ledit_seance.setText(self.allInfo[6])
        self.cabinet.setText(str(self.allInfo[3]))
        self.cost.setText(str(self.allInfo[7]))
        self.lastCost = self.allInfo[7]
        self.selectDates.hide()
        calendar = self.allInfo[1].split('-')
        self.date.setSelectedDate(datetime.date(year=int(calendar[0]),
                                                month=int(calendar[1]), day=int(calendar[2])))
        self.present.setText(str(self.allInfo[9]))
        timer = self.allInfo[2].split(':')
        self.time.setTime(datetime.time(hour=int(timer[0]), minute=int(timer[1])))
        self.timedelta.setCurrentText(CONST1[int(self.allInfo[-1])])
        self.doc_id = self.allInfo[4]
        self.pat_id = self.allInfo[5]
        self.seanceId = self.allInfo[0]
        attendance = self.costChanged()
        self.cursor.execute(f'''
                UPDATE seance SET attendance="{','.join([str(i) for i in attendance])}"
                WHERE seance_id={self.seanceId}''')
        self.db.commit()

    def paymentClicked(self):
        if self.changing:
            self.paying = Payment.SetPayment(self.allInfo[3], self.allInfo[2],
                                             self.allInfo[1], self.changingInfo[-1])
            self.paying.show()
            self.paying.exec_()
