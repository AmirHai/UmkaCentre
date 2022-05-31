from dialogCalendary import CalendarDialogWidget
from PyQt5 import uic
from AllConstants import *
from datetime import *
from seanceAdding import CreateSeance


class CalendarDays(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('../activities/weekdaysActivity.ui', self)
        self.setGeometry(0, Y_KORD, WINDOWWIDTH, WINDOWHEIGHT)
        self.setWindowTitle(CENTERNAME)
        self.setFixedSize(WINDOWWIDTH, WINDOWHEIGHT)

        self.date = date.today()

        self.db = sqlite3.connect('../data/seances.db')
        self.cursor = self.db.cursor()

        self.AllData = []
        self.Allscrolls = []

        self.dateOfSeances.clicked.connect(self.set_new_day)
        self.btn_addseance.clicked.connect(self.createSeance)
        self.rerollInfo.clicked.connect(self.download_day)

        self.download_day()

    def createSeance(self):
        self.newSeance = CreateSeance()
        self.newSeance.show()

    def set_new_day(self):
        newDate = CalendarDialogWidget.CalendarDialog(self.dateOfSeances)
        newDate.show()
        newDate.exec_()
        neededDate = self.dateOfSeances.text().split()
        mon = neededDate.pop(1)
        neededDate.insert(1, months[mon][1])
        self.date = '-'.join(reversed(neededDate))
        neededDate.pop(1)
        neededDate.insert(1, months[mon][0])
        self.dateOfSeances.setText(' '.join(neededDate))
        self.download_day()

    def download_day(self):
        for j in range(4):
            self.AllData.clear()

            self.Allscrolls.append(QScrollArea(self.allframes))
            self.Allscrolls[-1].resize(480, 850)
            self.Allscrolls[-1].move(480 * j, 40)
            self.Allscrolls[-1].show()
            self.Allscrolls[-1].setStyleSheet(funkstyle(*COLORS['scrollGrey']))
            self.Allscrolls[-1].setWidgetResizable(True)

            query = f""" SELECT * FROM seance WHERE day='{self.date}'
        AND cabinet={j + 1} """
            data = self.cursor.execute(query).fetchall()

            layout = QGridLayout()
            layout.setColumnMinimumWidth(0, 200)
            layout.setColumnMinimumWidth(1, 80)
            layout.setColumnMinimumWidth(2, 40)
            layout.setColumnMinimumWidth(3, 50)
            layout.setHorizontalSpacing(2)
            layout.setContentsMargins(0, 2, 0, 5)
            layout.setVerticalSpacing(5)

            timer = timedelta(hours=8)
            listWithTimes = {}

            for i in data:
                listWithTimes[timedelta(hours=int(i[2].split(':')[0]), minutes=int(i[2].split(':')[1]))] = (
                    i[5], i[6], i[7], i[9], i[8], i[10])

            willPassed = 0
            for i in range(25):
                if not willPassed:
                    if timer in listWithTimes:
                        willPassed = listWithTimes[timer][5] - 1
                    self.AllData.append([])
                    led = QLineEdit()
                    led.setFont(FONTFORWEEKS)
                    led.setReadOnly(True)
                    led.setStyleSheet(funkstyle(*COLORS['leditGrey']))
                    if timer in listWithTimes:
                        led.setText(' '.join(self.cursor.execute(f'''SELECT surname, name FROM patients WHERE 
                        patients_id = {listWithTimes[timer][0]} 
                         ''').fetchone()))
                    layout.addWidget(led, i, 0)
                    led = QLineEdit()
                    led.setFont(FONTFORWEEKS)
                    led.setReadOnly(True)
                    led.setStyleSheet(funkstyle(*COLORS['leditGrey']))
                    if timer in listWithTimes:
                        led.setText(listWithTimes[timer][1])
                    layout.addWidget(led, i, 1)
                    led = QLineEdit()
                    led.setFont(FONTFORWEEKS)
                    led.setReadOnly(True)
                    led.setStyleSheet(funkstyle(*COLORS['leditGrey']))
                    if timer.seconds >= TENHOURS:
                        led.setText(str(timer)[:5])
                    else:
                        led.setText(str(timer)[:4])
                    layout.addWidget(led, i, 2)
                    btn = QPushButton()
                    btn.setFont(FONTFORWEEKS)
                    btn.setStyleSheet(funkstyle(*COLORS['leditGrey']))
                    btn.setObjectName(f'btn;{j};{timer}')
                    if timer in listWithTimes:
                        btn.setText(str(listWithTimes[timer][2] - listWithTimes[timer][3]))
                        paying = sum(map(int, listWithTimes[timer][4].split(',')))
                        if paying == 0:
                            btn.setStyleSheet('''
                            background-color:rgb(225, 0, 0) ''')
                        elif paying < listWithTimes[timer][2] - listWithTimes[timer][3]:
                            btn.setStyleSheet('''
                            background-color:rgb(255, 223, 0) ''')
                        else:
                            btn.setStyleSheet('''
                            background-color:rgb(0, 225, 0) ''')
                    btn.clicked.connect(self.setOrViewPayment)
                    self.AllData.append(btn)
                    layout.addWidget(btn, i, 3)
                    timer += timedelta(minutes=30)
                else:
                    willPassed -= 1
                    timer += timedelta(minutes=30)

            widget = QWidget()
            widget.setLayout(layout)
            self.Allscrolls[-1].setWidget(widget)

    def setOrViewPayment(self):
        info = self.sender().objectName().split(';')
        info.pop(0)
        info[0] = str(int(info[0]) + 1)
        if len(info[1]) == 8:
            info[1] = info[1][:5]
        else:
            info[1] = '0' + info[1][:4]
        info.append(str(self.date))
        info.append(self.sender())
        self.changeSeance = CreateSeance(True, info)
        self.changeSeance.show()
