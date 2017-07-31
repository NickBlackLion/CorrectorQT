import MySQLdb as mdb
from PyQt5.QtCore import QRegExp


class Searcher:
    def __init__(self, centralW):
        self.doc = centralW.getDocument()
        self.cursor = centralW.getCursor()
        self.textArea = centralW.getTextArea()

    def searchAndMark(self, tableName, rgbColor=None):
        self.textDemark()

        allRegex = None
        con = mdb.connect('localhost', 'root', 'root', 'Corrector', charset="utf8")

        with con:
            cur = con.cursor()
            nameForTableLoad = None

            with open('categories', encoding='utf-8') as f:
                for value in f:
                    tableNameIns = value.split(';')
                    if tableNameIns[0] == tableName:
                        nameForTableLoad = tableNameIns[1].strip(' \n')

            if nameForTableLoad is not None:
                cur.execute('select * from {0}'.format(nameForTableLoad))
                allRegex = cur.fetchall()

        index = 0

        for val in allRegex:
            while index != -1:
                regex = QRegExp(val[1])
                curs = self.doc.find(regex, index)
                font = self.textArea.currentFont()
                print(font.pointSize(), font.family())
                self.doc.find(regex, index).insertHtml("<p style='background-color: #88B6FC;'>" + curs.selectedText()
                                                       + "</p>")
                self.textArea.setStyleSheet("QTextEdit {font-family: " + font.family() + "; font-size: "
                                            + str(font.pointSize()) + "pt}")
                index = curs.position()

    def textDemark(self):
        text = self.textArea.toPlainText()
        self.cursor.setPosition(1)
        font = self.cursor.blockCharFormat().font()
        self.textArea.clear()
        self.cursor.insertHtml('<body style="font-family: ' + font.family() + '">' + text + '</body>')
