from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QPushButton
import os
import importExportDB


class ExportImportWindow(QWidget):
    def __init__(self, imp=False):
        QWidget.__init__(self)
        self.imp = imp
        self.setWindowTitle('Экспорт базы данных')

        self.mainLayout = QVBoxLayout()

        self.label = QLabel()
        self.label.setMinimumWidth(200)
        self.label.setText(os.getcwd())

        self.passButton = QPushButton('...')
        self.passButton.clicked.connect(self.__getDidrectory)

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.label)
        self.layout1.addWidget(self.passButton)

        self.mainLayout.addLayout(self.layout1)

        self.okButton = QPushButton('Ok')
        self.okButton.clicked.connect(self.__makeExportImport)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.close)

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.okButton)
        self.layout2.addWidget(self.cancelButton)

        self.mainLayout.addLayout(self.layout2)

        self.setLayout(self.mainLayout)
        self.show()

    def __getDidrectory(self):
        if not self.imp:
            self.directoryName = QFileDialog.getExistingDirectory()

            if self.directoryName is not None and self.directoryName != '':
                self.label.setText(self.directoryName)

        else:
            self.directoryName = QFileDialog.getOpenFileName(self, '', '', "MySQL (*.sql)")
            if self.directoryName[0] is not None and self.directoryName != '':
                self.label.setText(self.directoryName[0])

    def __makeExportImport(self):
        if self.label.text() is not None and self.label.text() != '':
            importExportDB.makeImportExport(self.label.text(), self.imp)
            self.close()
