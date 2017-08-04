import MySQLdb as mdb
from PyQt5.QtCore import QRegExp


class Searcher:
    def __init__(self, centralW):
        self.doc = centralW.getDocument()
        self.cursor = centralW.getCursor()
        self.textArea = centralW.getTextArea()

        self.cursorPoints = []
        self.comments = {}

        self.category = None

    def searchAndMark(self):
        self.textDemark()

        allRegex = None
        con = mdb.connect('localhost', 'root', 'root', 'Corrector', charset="utf8")

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

        for val in allRegex:
            index = 0

            while index != -1:
                regex = QRegExp(val[1])
                font = self.textArea.textCursor().blockCharFormat().font()
                cursor = self.doc.find(regex, index)

                if cursor.position() != -1:
                    boundary = (cursor.position() - len(cursor.selectedText()), cursor.position())
                    self.comments[boundary] = val[2]
                    self.cursorPoints.append(boundary)

                cursor.insertHtml('<p style="background-color: #88B6FC; font-family: '
                                                       + font.family() + '; font-size: ' + str(font.pointSize())
                                                       + 'pt">' + cursor.selectedText() + "</p>")

                index = cursor.position()

            print(self.cursorPoints)

    def textDemark(self):
        text = self.textArea.toPlainText()
        cursor = self.textArea.textCursor()
        cursor.setPosition(3)
        font = cursor.blockCharFormat().font()
        self.textArea.clear()
        cursor.insertHtml('<body style="font-family: ' + font.family() + '; font-size: ' + str(font.pointSize())
                          + 'pt">' + text + '</body>')

        self.cursorPoints.clear()

    def getCursorPoints(self):
        return self.cursorPoints

    def getComments(self):
        return self.comments

    def setCategory(self, category):
        self.category = category