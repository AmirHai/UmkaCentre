import sys
from PyQt5.QtWidgets import QApplication
from expWeekDays import AllWindows


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AllWindows()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
