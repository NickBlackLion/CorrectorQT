import re
import MySQLdb as mdb
from PyQt5.QtGui import QTextDocument, QTextCursor


class Searcher:
    def __init__(self, centralW):
        self.doc = centralW.getDocument()
        self.cursor = centralW.getCursor()
        self.textArea = centralW.getTextArea()

    def searchAndMark(self, tableName):
        text = self.doc.toPlainText().split('\n')
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

        for value in text:
            for val in allRegex:
                result = re.findall(val[1], value)

                for key in result:
                    curs = self.doc.find(key)
                    print(curs.selectedText())
