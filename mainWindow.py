from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QPushButton
import sys
import fileMenu, editMenu, specialMenu, centralWidget
import shelve
import logging
import databaseConnect as dbCon
import additionalFunctions as addFoo

class MainWindow(QMainWindow):
    """Class that makes main window with all fillers"""
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.resize(1000, 500)
        self.move(100, 40)
        self.setWindowTitle('Корректор')
        self.app = app
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.isPressed = False

        with shelve.open('db_setup') as f:
            if len(f) == 0:
                f['host'] = 'localhost'
                f['name'] = 'root'
                f['password'] = 'root'
                f['db'] = 'Corrector'

        self.centralW = centralWidget.CentralWidget(self)

        self.__addCentralWidget()
        self.__addMenuBar()
        self.__addToolBar()

        self.dbc = dbCon.DBConnector(self)

        self.dbc.getConnection(True)
        with shelve.open('db_setup') as f:
            mysql = """create database if not EXISTS {0}
                                  DEFAULT CHARACTER set utf8
                                  DEFAULT COLLATE utf8_general_ci;""".format(f['db'])

        self.dbc.getCursorExecute(mysql)
        self.dbc.closeConnection()

        self.dbc.getConnection()
        with open('categories', encoding='utf-8') as f:
            for value in f:
                val = value.split(';')
                mysql = """create table if NOT EXISTS {0}(Id int PRIMARY KEY AUTO_INCREMENT,
                                      regex VARCHAR(255), comment longtext);""".format(val[1].strip(' \n'))
                self.dbc.getCursorExecute(mysql)
        self.dbc.closeConnection()
        self.show()

    def __addMenuBar(self):
        mainMenu = self.menuBar()
        self.fileMenu = fileMenu.FileMenu(app, self, mainMenu, self.centralW)
        editMenu.EditMenu(app, mainMenu, self.centralW)
        specialMenu.SpecialMenu(mainMenu, self.centralW)

    def __addToolBar(self):
        toolBar = self.addToolBar('Exit')

        self.fontFamily = QComboBox(toolBar)
        self.fontFamily.addItem('Times New Roman')
        self.fontFamily.activated.connect(self.__changeTextFamily)
        self.fontFamily.addItem('Segoe UI')

        self.changeTextStyle = addFoo.ChangeTextCharacteristics()

        sizeUpButton = QPushButton('A\u02c4')
        sizeUpButton.clicked.connect(lambda ev, area=self.centralW.getTextArea():
                                     self.changeTextStyle.increaseTextSize(area))
        sizeDownButton = QPushButton('a\u02c5')
        sizeDownButton.clicked.connect(lambda ev, area=self.centralW.getTextArea():
                                       self.changeTextStyle.decreaseTextSize(area))

        bButton = QPushButton('B', toolBar)
        bButton.setStyleSheet("QPushButton {font-weight: bold}")
        bButton.clicked.connect(self.__changeTextWeight)

        kButton = QPushButton('K', toolBar)
        kButton.setStyleSheet("QPushButton {font-style: italic}")
        kButton.clicked.connect(self.__changeTextStyle)

        iButton = QPushButton('I', toolBar)
        iButton.setStyleSheet("QPushButton {text-decoration: underline}")
        iButton.clicked.connect(self.__changeTextDecoration)

        killDoubleSpace = QPushButton('Убрать удвоенные пробелы')
        killDoubleSpace.clicked.connect(self.__delDoubleSpaces)

        unprintButton = QPushButton('\u00b6')
        unprintButton.clicked.connect(lambda ev, area=self.centralW.getTextArea():
                                           self.changeTextStyle.unprintableCharacters(area))

        toolBar.addWidget(self.fontFamily)
        toolBar.addWidget(sizeUpButton)
        toolBar.addWidget(sizeDownButton)
        toolBar.addSeparator()
        toolBar.addWidget(bButton)
        toolBar.addWidget(kButton)
        toolBar.addWidget(iButton)
        toolBar.addWidget(unprintButton)
        toolBar.addWidget(killDoubleSpace)

    def __addCentralWidget(self):
        self.setCentralWidget(self.centralW)

    def __changeTextFamily(self):
        cursor = self.centralW.getTextArea().textCursor()
        text = cursor.selectedText()
        font = cursor.charFormat().font()
        print(font.family(), font.pointSize())
        cursor.insertHtml('<p style="font-family: ' + self.fontFamily.currentText() + '; font-size: '
                          + str(font.pointSize()) + 'pt">' + text + '</p>')

    def __changeTextSize(self):
        cursor = self.centralW.getTextArea().textCursor()
        text = cursor.selectedText()
        font = cursor.charFormat().font()
        print(font.family(), font.pointSize())
        cursor.insertHtml('<p style="font-family: ' + font.family() + '; font-size: '
                          + self.fontSize.currentText() + 'pt">' + text + '</p>')

    def __changeTextWeight(self):
        cursor = self.centralW.getTextArea().textCursor()
        text = cursor.selectedText()
        font = cursor.charFormat().font()
        if not font.bold() and not font.italic() and not font.underline():
            cursor.insertHtml('<p style="font-weight: bold; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif not font.bold() and font.italic() and not font.underline():
            cursor.insertHtml('<p style="font-weight: bold; font-style: italic; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif not font.bold() and not font.italic() and font.underline():
            cursor.insertHtml('<p style="font-weight: bold; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif not font.bold() and font.italic() and font.underline():
            cursor.insertHtml('<p style="font-weight: bold; font-style: italic; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.bold() and not font.italic() and not font.underline():
            cursor.insertHtml('<p style="font-weight: normal;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.bold() and font.italic() and not font.underline():
            cursor.insertHtml('<p style="font-weight: normal; font-style: italic; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif font.bold() and not font.italic() and font.underline():
            cursor.insertHtml('<p style="font-weight: normal; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.bold() and font.italic() and font.underline():
            cursor.insertHtml('<p style="font-weight: normal; font-style: italic; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

    def __changeTextStyle(self):
        cursor = self.centralW.getTextArea().textCursor()
        text = cursor.selectedText()
        font = cursor.charFormat().font()
        if not font.italic() and not font.bold() and not font.underline():
            cursor.insertHtml('<p style="font-style: italic; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif not font.italic() and font.bold() and not font.underline():
            cursor.insertHtml('<p style="font-weight: bold; font-style: italic; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif not font.italic() and not font.bold() and font.underline():
            cursor.insertHtml('<p style="font-style: italic; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif not font.italic() and font.bold() and font.underline():
            cursor.insertHtml('<p style="font-style: italic; font-weight: bold; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.italic() and not font.bold() and not font.underline():
            cursor.insertHtml('<p style="font-style: normal;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.italic() and font.bold() and not font.underline():
            cursor.insertHtml('<p style="font-style: normal; font-weight: bold; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif font.italic() and not font.bold() and font.underline():
            cursor.insertHtml('<p style="font-style: normal; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.italic() and font.bold() and font.underline():
            cursor.insertHtml('<p style="font-style: normal; font-weight: bold; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

    def __changeTextDecoration(self):
        cursor = self.centralW.getTextArea().textCursor()
        text = cursor.selectedText()
        font = cursor.charFormat().font()
        if not font.underline() and not font.bold() and not font.italic():
            cursor.insertHtml('<p style="font-decoration: underline; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif not font.underline() and font.bold() and not font.italic():
            cursor.insertHtml('<p style="font-decoration: underline; font-weight: bold; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif not font.underline() and not font.bold() and font.italic():
            cursor.insertHtml('<p style="font-decoration: underline; font-style: italic;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif not font.underline() and font.bold() and font.italic():
            cursor.insertHtml('<p style="text-decoration: underline; font-style: italic; font-weight: bold;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.underline() and not font.bold() and not font.italic():
            cursor.insertHtml('<p style="text-decoration: none;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.underline() and font.bold() and not font.italic():
            cursor.insertHtml('<p style="text-decoration: none; font-weight: bold; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

        elif font.underline() and not font.bold() and font.italic():
            cursor.insertHtml('<p style="text-decoration: none; text-style: italic;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

        elif font.underline() and font.bold() and font.italic():
            cursor.insertHtml('<p style="text-decoration: none; font-weight: bold; text-decoration: underline;' +
                              'font-family: ' + font.family() + '; font-size: ' + str(font.pointSize()) + 'pt">'
                              + text + '</p>')

    def closeEvent(self, QCloseEvent):
        flag = self.fileMenu.saveIfChanged()
        if flag:
            QMainWindow.closeEvent(self, QCloseEvent)
        else:
            QCloseEvent.ignore()

    def __delDoubleSpaces(self):
        text = self.centralW.getTextArea().toHtml()
        text = text.replace('  ', ' ')
        text = text.replace('\u00b7\u00b7', '\u00b7')
        self.centralW.getTextArea().setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(app)
    sys.exit(app.exec_())
