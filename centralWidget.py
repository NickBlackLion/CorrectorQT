from PyQt5.QtWidgets import QWidget, QTextEdit, QGridLayout, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QTextDocument, QTextCursor


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
                category = word.strip('\n')
                categoryBox = QCheckBox(self)
                categoryBox.setText(category)
                categoryGrid.addWidget(categoryBox)

        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        categoryGrid.addItem(spacer)

        self.grid.addLayout(categoryGrid, 0, 1, 1, 1)

    def getDocument(self):
        return self.doc

    def getCursor(self):
        return self.cursor
