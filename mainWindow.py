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
            with open('tables', encoding='utf-8') as f:
                for value in f:
                    cur.execute("create table {0}(Id int PRIMARY KEY AUTO_INCREMENT, regex VARCHAR(255), comment VARCHAR(255));".format(value.strip('\n')))
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

        fontBox = QComboBox(toolBar)
        fontSize = QSpinBox(toolBar)

        bButton = QPushButton('B', toolBar)
        bButton.setStyleSheet("QPushButton {font-weight: bold}")

        kButton = QPushButton('K', toolBar)
        kButton.setStyleSheet("QPushButton {font-style: italic}")

        iButton = QPushButton('I', toolBar)
        iButton.setStyleSheet("QPushButton {text-decoration: underline}")

        toolBar.addWidget(fontBox)
        toolBar.addWidget(fontSize)
        toolBar.addSeparator()
        toolBar.addWidget(bButton)
        toolBar.addWidget(kButton)
        toolBar.addWidget(iButton)

    def __addCentralWidget(self):
        self.setCentralWidget(self.centralW)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(app)
    sys.exit(app.exec_())
