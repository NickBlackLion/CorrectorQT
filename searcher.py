import pymysql as mdb
from PyQt5.QtCore import QRegExp
from PyQt5.Qt import Qt
import shelve
import logging


class Searcher:
    """Class that makes searching through DB and highlight found concurrences"""
    def __init__(self, centralW):
        self.doc = centralW.getDocument()
        self.cursor = centralW.getCursor()
        self.textArea = centralW.getTextArea()

        self.cursorPoints = []
        self.comments = {}
        self.regexes = {}

        self.category = None

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def searchAndMark(self):
        """Function that highlight all found concurrences"""
        allRegex = self.__loadedBase()

        for val in allRegex:
            index = 0

            while index != -1:
                regex = QRegExp(val[1], Qt.CaseInsensitive)
                font = self.textArea.textCursor().blockCharFormat().font()
                cursor = self.doc.find(regex, index)

                if cursor.position() != -1:
                    boundary = (cursor.position() - len(cursor.selectedText()), cursor.position())
                    key = str(val[1]) + ';' + str(boundary)
                    self.comments[key] = val[2]
                    self.cursorPoints.append(key)
                    self.regexes[key] = cursor.selectedText()

                cursor.insertHtml('<p style="background-color: #88B6FC; font-family: '
                                                       + font.family() + '; font-size: ' + str(font.pointSize())
                                                       + 'pt">' + cursor.selectedText() + "</p>")

                index = cursor.position()

    def textDemark(self):
        """Function that take off highlight for all found concurrences"""
        allRegex = self.__loadedBase()

        for val in allRegex:
            index = 0

            while index != -1:
                regex = QRegExp(val[1], Qt.CaseInsensitive)
                font = self.textArea.textCursor().blockCharFormat().font()
                cursor = self.doc.find(regex, index)

                cursor.insertHtml('<p style="background-color: #ffffff; font-family: '
                                  + font.family() + '; font-size: ' + str(font.pointSize())
                                  + 'pt">' + cursor.selectedText() + "</p>")

                index = cursor.position()

        self.cursorPoints.clear()

    def selectedTextDemark(self, key, firstPoint):
        """Function that take off highlight for chose concurrence"""
        word = self.regexes[key]
        font = self.textArea.textCursor().blockCharFormat().font()
        cursor = self.doc.find(word, firstPoint)

        cursor.insertHtml('<p style="background-color: #ffffff; font-family: '
                                + font.family() + '; font-size: ' + str(font.pointSize())
                                + 'pt">' + cursor.selectedText() + "</p>")

    def deletePoints(self, key):
        self.cursorPoints.remove(key)
        del self.comments[key]

    def getCursorPoints(self):
        return self.cursorPoints

    def getComments(self):
        return self.comments

    def setCategory(self, category):
        self.category = category

    def __loadedBase(self):
        """Function that loads and makes connection to DB"""
        allRegex = None

        con = None
        with shelve.open('db_setup') as f:
            con = mdb.connect(f['host'], f['name'], f['password'], f['db'], charset="utf8")

        with con:
            cur = con.cursor()
            nameForTableLoad = None

            with open('categories', encoding='utf-8') as f:
                for value in f:
                    tableNameIns = value.split(';')
                    if tableNameIns[0] == self.category:
                        nameForTableLoad = tableNameIns[1].strip(' \n')

            if nameForTableLoad is not None:
                cur.execute('select * from {0}'.format(nameForTableLoad))
                allRegex = cur.fetchall()

        return allRegex