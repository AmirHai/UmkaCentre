from AllConstants import *
from WeekDays import CalendarDays
from PatientsRecearching import Patients


class AllWindows(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('Медицинский Центр Умка')

        self.AllWeeks = CalendarDays()

        self.patientWidget = QWidget()
        self.GridPatLayout = QGridLayout(self.patientWidget)
        self.GridPatLayout.addWidget(Patients('patients', self.GridPatLayout), 0, 0)

        self.doctorWidget = QWidget()
        self.GridDocLayout = QGridLayout(self.doctorWidget)
        self.GridDocLayout.addWidget(Patients('doctors', self.GridDocLayout), 0, 0)

        self.generalTabWidget = QTabWidget(self)
        self.generalTabWidget.setGeometry(0, 0, 1920, 1000)
        self.generalTabWidget.setFont(FONT)
        self.generalTabWidget.addTab(self.AllWeeks, 'Рассписание')
        self.generalTabWidget.addTab(self.patientWidget, 'Пациенты')
        self.generalTabWidget.addTab(self.doctorWidget, 'Доктора')

        self.showMaximized()


