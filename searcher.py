import pymysql as mdb
from PyQt5.QtCore import QRegExp
import shelve
import re


class Searcher:
    def __init__(self, centralW):
        self.doc = centralW.getDocument()
        self.cursor = centralW.getCursor()
        self.textArea = centralW.getTextArea()

        self.cursorPoints = []
        self.comments = {}
        self.regexes = {}

        self.category = None

    def searchAndMark(self):
        allRegex = self.__loadedBase()
        text = self.textArea.toPlainText()

        for val in allRegex:
            index = 0
            word = ''

            while index != -1:
                reg = re.search(val[1], text, re.IGNORECASE)

                if reg is not None:
                    word = text[reg.start():reg.end()]
                    text = text[reg.end():]

                regex = QRegExp(word)
                font = self.textArea.textCursor().blockCharFormat().font()
                cursor = self.doc.find(regex, index)

                if cursor.position() != -1:
                    boundary = (cursor.position() - len(cursor.selectedText()), cursor.position())
                    self.comments[boundary] = val[2]
                    self.cursorPoints.append(boundary)
                    self.regexes[boundary] = cursor.selectedText()

                cursor.insertHtml('<p style="background-color: #88B6FC; font-family: '
                                                       + font.family() + '; font-size: ' + str(font.pointSize())
                                                       + 'pt">' + cursor.selectedText() + "</p>")

                index = cursor.position()

    def textDemark(self):
        allRegex = self.__loadedBase()
        text = self.textArea.toPlainText()

        for val in allRegex:
            index = 0
            word = ''

            while index != -1:
                reg = re.search(val[1], text, re.IGNORECASE)

                if reg is not None:
                    word = text[reg.start():reg.end()]
                    text = text[reg.end():]

                regex = QRegExp(word)
                font = self.textArea.textCursor().blockCharFormat().font()
                cursor = self.doc.find(regex, index)

                cursor.insertHtml('<p style="background-color: #ffffff; font-family: '
                                  + font.family() + '; font-size: ' + str(font.pointSize())
                                  + 'pt">' + cursor.selectedText() + "</p>")

                index = cursor.position()

        self.cursorPoints.clear()

    def selectedTextDemark(self, points):
        word = self.regexes[points]
        font = self.textArea.textCursor().blockCharFormat().font()
        cursor = self.doc.find(word, points[0])

        cursor.insertHtml('<p style="background-color: #ffffff; font-family: '
                                + font.family() + '; font-size: ' + str(font.pointSize())
                                + 'pt">' + cursor.selectedText() + "</p>")

        self.cursorPoints.remove(points)
        del self.comments[points]

    def getCursorPoints(self):
        return self.cursorPoints

    def getComments(self):
        return self.comments

    def setCategory(self, category):
        self.category = category

    def __loadedBase(self):
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