from PyQt5.QtWidgets import QMenu, QAction


class EditMenu(QMenu):
    def __init__(self, parent, textArea):
        QMenu.__init__(self, parent)
        self.setTitle('Правка')
        parent.addMenu(self)

        self.__undoAction()
        self.__cupAction()
        self.__copyAction()
        self.__pasteAction()
        self.__findAction()

    def __undoAction(self):
        undoAction = QAction('Отменить', self)
        undoAction.setShortcut('Ctrl+Z')
        self.addAction(undoAction)
        self.addSeparator()

    def __cupAction(self):
        cupAction = QAction('Вырезать', self)
        cupAction.setShortcut('Ctrl+X')
        self.addAction(cupAction)

    def __copyAction(self):
        copyAction = QAction('Копировать', self)
        copyAction.setShortcut('Ctrl+С')
        self.addAction(copyAction)

    def __pasteAction(self):
        pasteAction = QAction('Вставить', self)
        pasteAction.setShortcut('Ctrl+V')
        self.addAction(pasteAction)
        self.addSeparator()

    def __findAction(self):
        findAction = QAction('Найти', self)
        findAction.setShortcut('Ctrl+F')
        self.addAction(findAction)
