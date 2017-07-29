from PyQt5.QtWidgets import QMenu, QAction
import dbCorrector


class SpecialMenu(QMenu):
    def __init__(self, parent, textArea):
        QMenu.__init__(self, parent)
        self.setTitle('Специальные функции')
        parent.addMenu(self)

        opendbCorrectorAction = QAction('База данных', self)
        opendbCorrectorAction.triggered.connect(self.__addDBCorrectoWindow)

        self.addAction(opendbCorrectorAction)

    def __addDBCorrectoWindow(self):
        dbCorrector.SpecialWidget()
