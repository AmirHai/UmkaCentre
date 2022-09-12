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
    '01': 'января',
    '02': 'февраля',
    '03': 'марта',
    '04': 'апреля',
    '05': 'мая',
    '06': 'июня',
    '07': 'июля',
    '08': 'августа',
    '09': 'сентября',
    '10': 'октября',
    '11': 'ноября',
    '12': 'декабря',
}

CONST = {
    'Полчаса': 1,
    'Час': 2,
    'Полтора часа': 3,
    'Два часа': 4,
}
CONST1 = {
    1: 'Полчаса',
    2: 'Час',
    3: 'Полтора часа',
    4: 'Два часа',
}


def RGB(r, g, b):
    return f'''
    background-color:rgb({r}, {g}, {b})
'''


# шпаргалка
# mod = {
# 'column'= ["=", "'", change, "'"] => "column='{}'".format(change)
# }
def getInfoFromDB(neededInfo, fromTable, mods=None, fetch='all', sumb='AND'):
    db = sqlite3.connect('../data/seances.db')
    cursor = db.cursor()
    result = [neededInfo, fromTable]
    query = ''' SELECT {} FROM {}'''
    if mods:
        query += ' WHERE '
        for i in list(mods.keys()):
            if len(mods[i]) == 4:
                result.append(i)
                result += mods[i]
                query += '{}{}{}{}{} '
            else:
                result.append(i)
                result += mods[i]
                query += '{}{}{} '
            if sumb == 'AND':
                query += 'AND '
            else:
                query += 'OR '
        query = query[0:-4]
    if fetch == 'all':
        Info = cursor.execute(query.format(*result)).fetchall()
    else:
        Info = cursor.execute(query.format(*result)).fetchone()
        db.close()
    return Info


def addInfoFromDB(table, columns, neededInfo):
    db = sqlite3.connect('../data/seances.db')
    cursor = db.cursor()
    query = f''' INSERT INTO {table} ({', '.join(columns)}) VALUES({str(neededInfo)[1:-1]}) '''
    cursor.execute(query)
    db.commit()
    db.close()


def updateInfoFromDB(table, columns, neededInfo, mods=None):
    db = sqlite3.connect('../data/seances.db')
    cursor = db.cursor()

    result = []
    dopquery = ""
    if mods:
        dopquery += " WHERE "
        for i in list(mods.keys()):
            if len(mods[i]) == 4:
                result.append(i)
                result += mods[i]
                dopquery += "{}{}{}{}{}"
            else:
                result.append(i)
                result += mods[i]
                dopquery += "{}{}{}"
            dopquery += " AND "
        dopquery = dopquery[0:-4]

    strform = """ UPDATE {} SET {}='{}' """ + dopquery
    intform = " UPDATE {} SET {}={} " + dopquery
    for i in range(len(columns)):
        changedInfo = [table, columns[i], neededInfo[i]]
        receivedList = changedInfo + result
        if type(neededInfo[i]) == 'int':
            cursor.execute(intform.format(*receivedList))
        else:
            cursor.execute(strform.format(*receivedList))
        db.commit()
    db.close()


def deleteInfoFromDB(table, mods=None):
    db = sqlite3.connect('../data/seances.db')
    cursor = db.cursor()

    query = ''' DELETE FROM {} '''
    result = [table]
    dopquery = ""
    if mods:
        dopquery += " WHERE "
        for i in list(mods.keys()):
            if len(mods[i]) == 4:
                result.append(i)
                result += mods[i]
                dopquery += "{}{}{}{}{}"
            else:
                result.append(i)
                result += mods[i]
                dopquery += "{}{}{}"
            dopquery += " AND "
        dopquery = dopquery[0:-4]
    query += dopquery
    cursor.execute(query.format(*result))
    db.commit()
    db.close()