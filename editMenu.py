from PyQt5.QtWidgets import QMenu, QAction


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
        findAction = QAction('Найти', self)
        findAction.setShortcut('Ctrl+F')
        self.addAction(findAction)
