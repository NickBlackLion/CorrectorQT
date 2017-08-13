from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QPushButton
import sys
import fileMenu, editMenu, specialMenu, centralWidget
import pymysql as mdb
import shelve


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.resize(1000, 500)
        self.move(100, 40)
        self.setWindowTitle('Корректор')
        self.app = app

        with shelve.open('db_setup') as f:
            if len(f) == 0:
                f['host'] = 'localhost'
                f['name'] = 'black'
                f['password'] = 'blacky13'
                f['db'] = 'Corrector'

        self.centralW = centralWidget.CentralWidget(self)

        self.__addCentralWidget()
        self.__addMenuBar()
        self.__addToolBar()

        con = None

        with shelve.open('db_setup') as f:
            con = mdb.connect(f['host'], f['name'], f['password'], f['db'], charset="utf8")

        try:
            cur = con.cursor()
            with open('categories', encoding='utf-8') as f:
                for value in f:
                    val = value.split(';')
                    cur.execute("create table if NOT EXISTS {0}(Id int PRIMARY KEY AUTO_INCREMENT, regex VARCHAR(255), comment VARCHAR(255));".format(val[1].strip(' \n')))
        except mdb.Error:
            print('Tables already exist')

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

        self.fontSize = QComboBox(toolBar)
        for i in range(6, 31):
            self.fontSize.addItem(str(i))
        self.fontSize.activated.connect(self.__changeTextSize)

        bButton = QPushButton('B', toolBar)
        bButton.setStyleSheet("QPushButton {font-weight: bold}")
        bButton.clicked.connect(self.__changeTextWeight)

        kButton = QPushButton('K', toolBar)
        kButton.setStyleSheet("QPushButton {font-style: italic}")

        iButton = QPushButton('I', toolBar)
        iButton.setStyleSheet("QPushButton {text-decoration: underline}")

        toolBar.addWidget(self.fontFamily)
        toolBar.addWidget(self.fontSize)
        toolBar.addSeparator()
        toolBar.addWidget(bButton)
        toolBar.addWidget(kButton)
        toolBar.addWidget(iButton)

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
        if not font.bold():
            cursor.insertHtml('<p style="font-weight: bold; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')
        else:
            cursor.insertHtml('<p style="font-weight: normal; font-family: ' + font.family()
                              + '; font-size: ' + str(font.pointSize()) + 'pt">' + text + '</p>')

    def closeEvent(self, QCloseEvent):
        flag = self.fileMenu.saveIfChanged()
        if flag:
            QMainWindow.closeEvent(self, QCloseEvent)
        else:
            QCloseEvent.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(app)
    sys.exit(app.exec_())
