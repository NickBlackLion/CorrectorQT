from PyQt5.QtWidgets import QMenu, QAction, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.Qt import QTextCursor


class EditMenu(QMenu):
    """Class that provides standard functions like: cut, copy, paste, find"""
    def __init__(self, app, parent, centralW):
        QMenu.__init__(self, parent)
        self.setTitle('Правка')
        parent.addMenu(self)

        self.parent = parent
        self.doc = centralW.getDocument()
        self.cursor = centralW.getCursor()
        self.app = app
        self.textArea = centralW.getTextArea()

        self.__undoAction()
        self.__redoAction()
        self.__cutAction()
        self.__copyAction()
        self.__pasteAction()
        self.__findAction()

    def __undoAction(self):
        self.undoAction = QAction('Отменить', self)
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.triggered.connect(self.doc.undo)
        self.addAction(self.undoAction)

    def __redoAction(self):
        self.redoAction = QAction('Вернуть', self)
        self.redoAction.setShortcut('Ctrl+Y')
        self.redoAction.triggered.connect(self.doc.redo)
        self.addAction(self.redoAction)
        self.addSeparator()

    def __cutAction(self):
        self.cutAction = QAction('Вырезать', self)
        self.cutAction.setShortcut('Ctrl+X')
        self.cutAction.triggered.connect(self.textArea.cut)
        self.addAction(self.cutAction)

    def __copyAction(self):
        self.copyAction = QAction('Копировать', self)
        self.copyAction.setShortcut('Ctrl+С')
        self.copyAction.triggered.connect(self.textArea.copy)
        self.addAction(self.copyAction)

    def __pasteAction(self):
        self.pasteAction = QAction('Вставить', self)
        self.pasteAction.setShortcut('Ctrl+V')
        self.pasteAction.triggered.connect(self.textArea.paste)
        self.addAction(self.pasteAction)
        self.addSeparator()

    def __findAction(self):
        self.findAction = QAction('Найти', self)
        self.findAction.setShortcut('Ctrl+F')
        self.findWind = FindWindow(self.textArea)
        self.findAction.triggered.connect(lambda: self.findWind.show())
        self.addAction(self.findAction)


class FindWindow(QWidget):
    def __init__(self, textArea):
        QWidget.__init__(self)
        self.setWindowTitle('Найти')
        self.mainlayout = QVBoxLayout()
        self.textArea = textArea

        self.lineEdit = QLineEdit()
        self.lineEdit.setMinimumWidth(250)

        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton('Найти')
        self.okButton.clicked.connect(self.__findAction)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.close)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)

        self.mainlayout.addWidget(self.lineEdit)
        self.mainlayout.addLayout(buttonLayout)

        self.setLayout(self.mainlayout)

    def __findAction(self):
        text = self.lineEdit.text()
        if text != '':
            found = self.textArea.find(text)
            if not found:
                cursor = QTextCursor()
                cursor.atStart()
                self.textArea.setTextCursor(cursor)
