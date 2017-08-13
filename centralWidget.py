from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtCore import Qt
from searcher import Searcher
from myTextArea import TextArea


class CentralWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.textArea = TextArea()

        self.doc = QTextDocument(self)
        self.cursor = QTextCursor(self.doc)

        self.textArea.setDocument(self.doc)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.textArea)

        self.categoryGrid = QVBoxLayout(self)

        self.__addCategoryMenu()

        self.setLayout(self.grid)

        self.se = Searcher(self)
        self.textArea.setSE(self.se)
        self.textArea.setCategoryGrid(self.categoryGrid)

    def __addCategoryMenu(self):
        with open('categories', encoding='utf-8') as f:
            for (index, word) in enumerate(f):
                category = word.split(';')
                categoryBox = QCheckBox(self)
                categoryStripped = category[0].strip('\n')
                categoryBox.setText(categoryStripped)
                categoryBox.stateChanged.connect(lambda a, b=categoryStripped: self.makeSearch(a, b))
                self.categoryGrid.addWidget(categoryBox)

        spacerV = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacerH = QSpacerItem(350, 1, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.categoryGrid.addItem(spacerV)
        self.categoryGrid.addItem(spacerH)

        self.grid.addLayout(self.categoryGrid, 0, 1, 1, 1)

    def getDocument(self):
        return self.doc

    def getCursor(self):
        return self.cursor

    def getTextArea(self):
        return self.textArea

    def makeSearch(self, state, category):
        self.se.setCategory(category)
        if state == Qt.Checked:
            self.se.searchAndMark()
        else:
            self.se.textDemark()
