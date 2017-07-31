from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QSpinBox, QPushButton
import sys
import fileMenu, editMenu, specialMenu, centralWidget
import MySQLdb as mdb


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.resize(800, 500)
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
        cursor.insertHtml('<body style="font-family: ' + self.fontFamily.currentText() + '">' + text + '</body>')

    def __changeTextSize(self):
        cursor = self.centralW.getTextArea().textCursor()
        text = cursor.selectedText()
        cursor.insertHtml('<body style="font-size: ' + self.fontSize.currentText() + 'pt">' + text + '</body>')

    def __changeTextWeight(self):
        cursor = self.centralW.getTextArea().textCursor()
        text = cursor.selectedText()
        print(cursor.charFormat().font().bold())
        if not cursor.charFormat().font().bold():
            cursor.insertHtml('<body style="font-weight: bold">' + text + '</body>')
        else:
            cursor.insertHtml('<body style="font-weight: normal">' + text + '</body>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(app)
    sys.exit(app.exec_())
