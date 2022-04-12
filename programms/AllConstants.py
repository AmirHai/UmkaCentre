from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import PyQt5.QtCore
import sqlite3

WINDOWWIDTH = 1920
WINDOWHEIGHT = 1000
MENUWIDTH = 320
MENUHEIGHT = 280
X_MENU_KORD = 0
X_KORD = 320
Y_KORD = 30
CENTERNAME = 'Центр Умка'
FONT = QFont()
FONT.setPointSize(12)
FONTFORWEEKS = QFont()
FONTFORWEEKS.setPointSize(10)
TENHOURS = 60 * 60 * 10

COLORS = {
    'leditGrey': [234, 234, 234],
    'scrollGrey': [200, 200, 200],
    'redbtn': [225, 0, 0],
    'yellowbtn': [255, 223, 0],
    'greenbtn': [0, 225, 0]

}
months = {
    'January': ('января', '01'),
    'February': ('февраля', '02'),
    'March': ('марта', '03'),
    'April': ('апреля', '04'),
    'May': ('мая', '05'),
    'June': ('июня', '06'),
    'July': ('июля', '07'),
    'August': ('августа', '08'),
    'September': ('сентября', '09'),
    'October': ('октября', '10'),
    'November': ('ноября', '11'),
    'December': ('декабря', '12'),

}


def funkstyle(r, g, b):
    return f'''
    background-color:rgb({r}, {g}, {b})
'''
