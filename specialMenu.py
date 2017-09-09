from PyQt5.QtWidgets import QMenu, QAction
import dbCorrector
import exportMenu


class SpecialMenu(QMenu):
    def __init__(self, parent, textArea):
        QMenu.__init__(self, parent)
        self.setTitle('Специальные функции')
        parent.addMenu(self)

        opendbCorrectorAction = QAction('База данных', self)
        opendbCorrectorAction.triggered.connect(self.__addDBCorrectoWindow)

        exportDBAction = QAction('Экспорт базы данных', self)
        exportDBAction.triggered.connect(self.__addExportWindow)

        importDBAction = QAction('Импорт базы данных', self)
        importDBAction.triggered.connect(self.__addImportWindow)

        self.addAction(opendbCorrectorAction)
        self.addAction(exportDBAction)
        self.addAction(importDBAction)

    def __addDBCorrectoWindow(self):
        self.specWidget = dbCorrector.SpecialWidget()

    def __addExportWindow(self):
        self.exportWidget = exportMenu.ExportImportWindow()

    def __addImportWindow(self):
        self.importWidget = exportMenu.ExportImportWindow(imp=True)
