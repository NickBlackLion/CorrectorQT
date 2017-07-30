from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtCore import Qt
from searcher import Searcher


class CentralWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.textArea = QTextEdit(self)

        self.doc = QTextDocument(self)
        self.cursor = QTextCursor(self.doc)

        self.textArea.setDocument(self.doc)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.textArea)

        self.__addCategoryMenu()

        self.setLayout(self.grid)

    def __addCategoryMenu(self):
        categoryGrid = QVBoxLayout(self)
        with open('categories', encoding='utf-8') as f:
            for (index, word) in enumerate(f):
                category = word.split(';')
                categoryBox = QCheckBox(self)
                categoryStripped = category[0].strip('\n')
                categoryBox.setText(categoryStripped)
                categoryBox.stateChanged.connect(lambda a, b=categoryStripped: self.makeSearch(a, b))
                categoryGrid.addWidget(categoryBox)

        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        categoryGrid.addItem(spacer)

        self.grid.addLayout(categoryGrid, 0, 1, 1, 1)

    def getDocument(self):
        return self.doc

    def getCursor(self):
        return self.cursor

    def getTextArea(self):
        return self.textArea

    def makeSearch(self, state, category):
        if state == Qt.Checked:
            se = Searcher(self)
            se.searchAndMark(category)
