from PyQt5.QtWidgets import QTableWidget, QMessageBox, QWidget,\
    QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit, QLabel, QComboBox
import shelve
import pymysql as mdb


class SpecialWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Работа с базой данных')

        self.resize(1100, 300)
        self.mainLayout = QHBoxLayout()

        self.titles = ['Гласные', 'Согласные', 'Глухие согласные',
                       'Пробел', '"Другие буквы"', 'Удвоение', '"Или"', 'Любой символ', 'Цифра', 'Точка',
                       'Граница слова', 'Граница слова \n-Или-\n Граница слова']

        self.commandsArray = ['[аеєиіїоуюя]', '[бвгґджзйклмнпрстфхцчшщ]', '[пхктшчсц]',
                              '\\\\s', '\\\\w+', '{2}', '|', '.', '[0-9]', '\\.', '\\\\b', '\\\\b|\\\\b']

        self.__createTable()
        self.__createTextFilds()
        self.__createButtons()

        self.id = None

        self.setLayout(self.mainLayout)
        self.show()

    def __createTable(self):
        layout1 = QHBoxLayout()
        self.box = QComboBox()

        with open('categories', encoding='utf-8') as f:
            for item in f:
                itemList = item.split(';')
                self.box.addItem(itemList[0])

        loadButton = QPushButton('Загрузить')
        loadButton.clicked.connect(lambda: self.__uploadDataToTable(self.box.currentText()))

        layout1.addWidget(self.box)
        layout1.addWidget(loadButton)

        self.table = QTableWidget()
        layout2 = QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(self.table)

        self.mainLayout.addLayout(layout2)

    def __createTextFilds(self):
        lab1 = QLabel('Шаблон поиска')
        lab2 = QLabel('Комментрий')

        self.patternArea = QTextEdit()
        self.hintArea = QTextEdit()

        self.createButton = QPushButton('Добавить')
        self.createButton.clicked.connect(lambda: self.__insertDataToDB(self.box.currentText()))
        self.correctButton = QPushButton('Редактировать')
        self.correctButton.clicked.connect(lambda: self.__updateDataInRow(self.box.currentText()))
        self.deleteButton = QPushButton('Удалить')
        self.deleteButton.clicked.connect(lambda: self.__deleteDataFromTable(self.box.currentText()))
        self.cancelButton = QPushButton('Отменить')
        self.cancelButton.clicked.connect(lambda: self.__cancelAction())

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.createButton)
        buttonLayout.addWidget(self.correctButton)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.cancelButton)

        layout = QVBoxLayout()
        layout.addWidget(lab1)
        layout.addWidget(self.patternArea)
        layout.addWidget(lab2)
        layout.addWidget(self.hintArea)
        layout.addLayout(buttonLayout)
        self.mainLayout.addLayout(layout)

    def __createButtons(self):
        layout = QVBoxLayout()

        for index, value in enumerate(self.titles):
            butt = QPushButton(value)
            butt.clicked.connect(lambda x, y=self.commandsArray[index].strip('\n'): self.__takeStrings(y))
            layout.addWidget(butt)

        self.mainLayout.addLayout(layout)

    def __takeStrings(self, mark):
        self.patternArea.insertPlainText(mark)

    def __loadData(self, categoryName):
        connectionData = self.__connectionToDB(categoryName)

        connectionData[1].execute('select * from {0}'.format(connectionData[2]))
        allRegex = connectionData[1].fetchall()

        return allRegex

    def __uploadDataToTable(self, categoryName):
        data = self.__loadData(categoryName)

        if len(data) == 0:
            QMessageBox.information(self, 'Инфо', 'База данных пустая')
            self.table.clear()
            return

        self.table.setColumnCount(len(data[0]))
        self.table.setRowCount(len(data))

        for table_row_index, table_row in enumerate(data):
            for table_column_index, table_cell_value in enumerate(table_row):
                self.table.setItem(table_row_index, table_column_index, QTableWidgetItem(str(table_cell_value)))

        self.table.setHorizontalHeaderLabels(('Id', 'Шаблон', 'Комментарий'))
        self.table.itemClicked.connect(lambda: self.__setDataToAreas())

        self.patternArea.clear()
        self.hintArea.clear()

    def __setDataToAreas(self):
        for i in self.table.selectedItems():
            if i.column() == 0:
                self.id = self.table.item(i.row(), i.column()).text()
                self.patternArea.clear()
                self.patternArea.append(self.table.item(i.row(), (i.column()+1)).text())
                self.hintArea.clear()
                self.hintArea.append(self.table.item(i.row(), (i.column()+2)).text())

    def __insertDataToDB(self, tableName):
        connectionData = self.__connectionToDB(tableName)

        if self.patternArea.toPlainText() != '':
            mysql = "insert into `{0}` SET `regex`='{1}', `comment` = '{2}'".format(connectionData[2],
                                                                                    self.patternArea.toPlainText(),
                                                                                    self.hintArea.toPlainText())
            connectionData[1].execute(mysql)
            connectionData[0].commit()

            self.__uploadDataToTable(tableName)
            self.patternArea.cursor()
            self.hintArea.clear()
        else:
            QMessageBox.information(self, 'Инфо', 'Добавьте регекс для внесения в базу данных')

    def __updateDataInRow(self, tableName):
        connectionData = self.__connectionToDB(tableName)

        if self.id is not None:
            mysql = "UPDATE `{0}` SET `regex`='{1}', `comment` = '{2}' WHERE `Id` = {3}".format(connectionData[2],
                                                                                                self.patternArea.toPlainText(),
                                                                                                self.hintArea.toPlainText(),
                                                                                                self.id)

            connectionData[1].execute(mysql)
            connectionData[0].commit()

            self.__uploadDataToTable(tableName)
            self.id = None
            self.patternArea.cursor()
            self.hintArea.clear()
        else:
            QMessageBox.information(self, 'Инфо', 'Выберите строку для изменения')

    def __deleteDataFromTable(self, tableName):
        connectionData = self.__connectionToDB(tableName)

        if self.id is not None:
            dialog = QMessageBox.question(self, 'Удаление', 'Вы действительно хотите удалить запись?')
            if dialog == QMessageBox.Yes:
                mysql = "DELETE FROM `{0}` WHERE `Id` = {1}".format(connectionData[2], self.id)

                connectionData[1].execute(mysql)
                connectionData[0].commit()

                self.__uploadDataToTable(tableName)
                self.id = None
                self.patternArea.cursor()
                self.hintArea.clear()
        else:
            QMessageBox.information(self, 'Инфо', 'Выберите строку для удаления')

    def __cancelAction(self):
        self.patternArea.clear()
        self.hintArea.clear()
        self.id = None

    def __connectionToDB(self, tableName):
        con = None
        nameForTableLoad = ''

        with shelve.open('db_setup') as f:
            con = mdb.connect(f['host'], f['name'], f['password'], f['db'], charset="utf8")

        with con:
            cur = con.cursor()

            with open('categories', encoding='utf-8') as f:
                for value in f:
                    tableNameIns = value.split(';')
                    if tableNameIns[0] == tableName:
                        nameForTableLoad = tableNameIns[1].strip(' \n')

        return con, cur, nameForTableLoad
