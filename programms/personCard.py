from AllConstants import *
from PyQt5 import uic
from LastSeancesInfo import LastSeances
import sqlite3


class PersonCard(QWidget):
    def __init__(self, p_id):
        super().__init__()
        self.setGeometry(X_KORD, Y_KORD, 950, 1000)
        self.setFixedSize(950, 950)
        uic.loadUi('../activities/personCardWindow.ui', self)
        self.setWindowTitle(f'карточка пациента')
        self.Activated = False
        self.patients_ID = p_id
        self.redactor_rbtn.setChecked(False)
        self.RbtnClicked()
        self.downloadAllInfo()
        self.redactor_rbtn.toggled.connect(self.RbtnClicked)
        self.SaveInfoBtn.clicked.connect(self.saveInfo)
        self.btn_seances.clicked.connect(self.LastSeances)

    def RbtnClicked(self):
        self.Activated = not self.Activated
        self.ledit_FIO.setReadOnly(self.Activated)
        self.birthCertificateText1.setReadOnly(self.Activated)
        self.birthCertificateText2.setReadOnly(self.Activated)
        self.birthday_ledit.setReadOnly(self.Activated)
        self.ledit_address.setReadOnly(self.Activated)
        self.ledit_parents_FIO.setReadOnly(self.Activated)
        self.ledit_phoneNumb.setReadOnly(self.Activated)
        self.PasportSeria.setReadOnly(self.Activated)
        self.PasportNumb.setReadOnly(self.Activated)
        self.gettingData.setReadOnly(self.Activated)
        self.sectionPoz.setReadOnly(self.Activated)
        self.whereGot.setReadOnly(self.Activated)
        self.moneyOnProfile.setReadOnly(self.Activated)

    def downloadAllInfo(self):
        try:
            self.file = open(f'../data/patients/ID{self.patients_ID[0]}.txt', 'r', encoding='utf-8')
        except FileNotFoundError:
            self.file = open(f'../data/patients/ID{self.patients_ID[0]}.txt', 'w+', encoding='utf-8')
            self.file.close()
            self.file = open(f'../data/patients/ID{self.patients_ID[0]}.txt', 'r', encoding='utf-8')
        info = self.file.readlines()
        # ФИО, дата рождения, ФИО Родителей, адрес, номер телефона, свидетельство о рождении, свидетельства
        self.moneyOnProfile.setText(
            str(getInfoFromDB('money', 'patients', {'patients_id': ['=', self.patients_ID[0]]}, 'one')[0]))
        try:
            self.ledit_FIO.setText(info[0])
            self.birthday_ledit.setText(info[1])
            self.ledit_parents_FIO.setText(info[2])
            self.ledit_address.setText(info[3])
            self.ledit_phoneNumb.setText(info[4])
            self.birthCertificateText1.setText(info[5])
            self.birthCertificateText2.setText(info[6])
            self.PasportSeria.setText(info[7])
            self.PasportNumb.setText(info[8])
            self.gettingData.setText(info[9])
            self.sectionPoz.setText(info[10])
            self.whereGot.setText('\n'.join(info[11::]))
        except IndexError:
            # тк в файле прост нет информации
            pass

    def saveInfo(self):
        self.file = open(f'../data/patients/ID{self.patients_ID[0]}.txt', 'w', encoding='utf-8')
        savingFile = [self.ledit_FIO.text().strip(),
                      self.birthday_ledit.text().strip(),
                      self.ledit_parents_FIO.text().strip(),
                      self.ledit_address.text().strip(),
                      self.ledit_phoneNumb.text().strip(),
                      self.birthCertificateText1.text().strip(),
                      self.birthCertificateText2.text().strip(),
                      self.PasportSeria.text().strip(),
                      self.PasportNumb.text().strip(),
                      self.gettingData.text().strip(),
                      self.sectionPoz.text().strip(),
                      self.whereGot.toPlainText().strip()]
        self.file.write('\n'.join(savingFile))
        self.file.close()
        updateInfoFromDB('patients', ['money'], [int(self.moneyOnProfile.text())],
                         {'patients_id': ['=', self.patients_ID[0]]})

    def LastSeances(self):
        self.seance = LastSeances(self.patients_ID)
        self.seance.show()


# --------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------

class DoctorsCard(QWidget):
    def __init__(self, d_id):
        super().__init__()
        self.setGeometry(X_KORD, Y_KORD, 950, 950)
        self.setFixedSize(950, 950)
        uic.loadUi('../activities/doctorCardWindow.ui', self)
        self.setWindowTitle(f'карточка доктора')
        self.Activated = False
        self.doctors_ID = d_id
        self.redactor_rbtn.setChecked(False)

        self.database = sqlite3.connect('../data/seances.db')
        self.cursor = self.database.cursor()

        self.RbtnClicked()
        self.downloadAllInfo()
        self.redactor_rbtn.toggled.connect(self.RbtnClicked)
        self.SaveInfoBtn.clicked.connect(self.saveInfo)

    def RbtnClicked(self):
        self.Activated = not self.Activated
        self.ledit_FIO.setReadOnly(self.Activated)
        self.ledit_special.setReadOnly(self.Activated)
        self.ledit_lastWork.setReadOnly(self.Activated)
        self.ledit_phoneNumb.setReadOnly(self.Activated)

    def downloadAllInfo(self):
        try:
            self.file = open(f'../data/doctors/ID{self.doctors_ID[0]}.txt', 'r', encoding='utf-8')
        except FileNotFoundError:
            self.file = open(f'../data/doctors/ID{self.doctors_ID[0]}.txt', 'w+', encoding='utf-8')
            self.file.close()
            self.file = open(f'../data/doctors/ID{self.doctors_ID[0]}.txt', 'r', encoding='utf-8')
        info = self.file.readlines()
        # ФИО, дата рождения, адрес, номер телефона, рабочие данные
        try:
            self.ledit_FIO.setText(info[0])
            self.ledit_special.setText(info[1])
            self.ledit_lastWork.setText(info[2])
            self.ledit_phoneNumb.setText(info[3])

        except IndexError:
            # тк в файле прост нет информации
            pass

    def saveInfo(self):
        self.file = open(f'../data/doctors/ID{self.doctors_ID[0]}.txt', 'w', encoding='utf-8')
        savingFile = ''
        savingFile += self.ledit_FIO.text()
        savingFile += self.ledit_special.text()
        savingFile += self.ledit_lastWork.text()
        savingFile += self.ledit_phoneNumb.text()
        self.file.write(savingFile)
