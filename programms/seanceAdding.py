from AllConstants import *
from dialogResearching import selectInputFromDB
from PyQt5 import uic


class CreateSeance(QWidget):
    def __init__(self):
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

        self.Doctors.clicked.connect(self.researching)
        self.Patients.clicked.connect(self.researching)
        self.seanceType.clicked.connect(self.researching)
        self.btn_add.clicked.connect(self.addSeancePressed)

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
        Id = len(self.cursor.execute(''' SELECT * FROM seance ''').fetchall()) + 1
        time = self.time.time().toString('HH:mm')
        if self.present.text() == '':
            present = 0
        else:
            present = int(self.present.text())
        if self.doc_id and self.pat_id and self.ledit_seance.text() and self.cabinet.text() and self.cost.text():
            for i in self.AllDates:
                attendance = self.MoneyExamination()
                query = f''' INSERT INTO seance (seance_id, day, time, cabinet, 
                doctor, patient, seanceType, cost, attendance, discount, deltatime)
                VALUES ({Id}, "{i}", "{time}", {int(self.cabinet.text())}, {self.doc_id}, {self.pat_id},
                "{self.ledit_seance.text()}", {int(self.cost.text())}, "{attendance}",
                {present}, {CONST[self.timedelta.currentText()]}); '''
                self.cursor.execute(query)
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