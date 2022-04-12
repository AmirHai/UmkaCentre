from PyQt5 import uic
from AllConstants import *
from PatientsRecearching import Patients
import WeekDays


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('../activities/MenuActivity.ui', self)
        self.setGeometry(X_MENU_KORD, Y_KORD, MENUWIDTH, MENUHEIGHT)
        self.setFixedSize(MENUWIDTH, MENUHEIGHT)
        self.setWindowTitle(CENTERNAME)

        self.btn_openCalendar.clicked.connect(self.OpenCalendar)
        self.btn_allPatients.clicked.connect(self.OpenAllPatients)
        self.btn_allDoctors.clicked.connect(self.OpenAllDoctors)

    def OpenCalendar(self):
        self.calend = WeekDays.CalendarDays()
        self.calend.show()

    def OpenAllPatients(self):
        self.researchPatientsSystem = Patients('patients')
        self.researchPatientsSystem.show()

    def OpenAllDoctors(self):
        self.researchDoctorsSystem = Patients('doctors')
        self.researchDoctorsSystem.show()
