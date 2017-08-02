from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QSpinBox, QPushButton
import sys
import fileMenu, editMenu, specialMenu, centralWidget
import MySQLdb as mdb


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.resize(1000, 500)
        self.move(100, 40)
        self.setWindowTitle('Корректор')
        self.app = app

        self.centralW = centralWidget.CentralWidget(self)

        self.__addCentralWidget()
        self.__addMenuBar()
        self.__addToolBar()

        con = mdb.connect('localhost', 'root', 'root', 'Corrector')

        try:
            cur = con.cursor()
            with open('categories', encoding='utf-8') as f:
                for value in f:
                    val = value.split(';')
                    cur.execute("create table {0}(Id int PRIMARY KEY AUTO_INCREMENT, regex VARCHAR(255), comment VARCHAR(255));".format(val[1].strip(' \n')))
        except mdb.Error:
            print('Tables already exist')

        self.show()

    def __addMenuBar(self):
        mainMenu = self.menuBar()
        fileMenu.FileMenu(app, self, mainMenu, self.centralW)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(app)
    sys.exit(app.exec_())
