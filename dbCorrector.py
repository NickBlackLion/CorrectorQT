# coding: utf8
from PyQt5.QtWidgets import QTableWidget, QMessageBox, QWidget,\
QTableWidgetItem, QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit,\
    QLabel, QComboBox, QLineEdit, QHeaderView, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
import shelve
import pymysql as mdb


class SpecialWidget(QWidget):
    """Class that creates new window in that you can work with database:
    create, update and delete regex from DB"""
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Работа с базой данных')

        self.resize(1100, 300)
        self.mainLayout = QHBoxLayout()

        """self.titles = ['\\s[^\\.]{,40}\\s?', 'Гласные', 'Согласные', 'Глухие согласные',
                       'Пробел', '"Другие буквы"', 'Удвоение', '"Или"', 'Любой символ', 'Цифра', 'Точка',
                       'Граница слова', 'Граница слова \n-Или-\n Граница слова']"""

        self.titles = ['\\s[^\\.]{,40}\\s?', 'Гласные', 'Согласные', 'Глухие согласные']

        """self.commandsArray = [ '\\s[^\\.]{,40}\\s?', '[аеєиіїоуюя]', '[бвгґджзйклмнпрстфхцчшщь]', '[пхктшчсц]',
                              '\\s', '\\w+', '{2}', '|', '.', '[0-9]', '\\.', '\\b', '\\b|\\b']"""

        self.commandsArray = ['\\s[^\\.]{,40}\\s?', '[аеєиіїоуюя]', '[бвгґджзйклмнпрстфхцчшщь]', '[пхктшчсц]']

        self.__createTable()
        self.__DBControlButtons()
        self.__createTextFilds()
        self.__createButtons()

        self.dataInTable = None
        self.id = None
        self.counter = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.__ifPresentInDB)
        self.timer.start(50)

        self.setLayout(self.mainLayout)
        self.show()

    def __createTable(self):
        """Method that creates first layout with list of tables in DB, load and find buttons"""
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

        findLayout = QHBoxLayout()
        findLine = QLineEdit()

        findButton = QPushButton('Найти')
        findButton.clicked.connect(lambda: self.__searchForCoincidence(findLine.text(), self.box.currentText()))

        findLayout.addWidget(findLine)
        findLayout.addWidget(findButton)

        self.table = QTableWidget()
        self.layout2 = QVBoxLayout()
        self.layout2.addLayout(layout1)
        self.layout2.addLayout(findLayout)
        self.layout2.addWidget(self.table)

        self.mainLayout.addLayout(self.layout2)

    def __DBControlButtons(self):
        """Method that creates buttons for 'CRUD' actions in DB"""
        self.createButton = QPushButton('Добавить')
        self.createButton.clicked.connect(lambda: self.__insertDataToDB(self.box.currentText()))
        self.correctButton = QPushButton('Редактировать')
        self.correctButton.clicked.connect(lambda: self.__updateDataInRow(self.box.currentText()))
        self.deleteButton = QPushButton('Удалить')
        self.deleteButton.clicked.connect(lambda: self.__deleteDataFromTable(self.box.currentText()))
        self.cancelButton = QPushButton('Отменить')
        self.cancelButton.clicked.connect(lambda: self.__cancelAction())

        spacerV = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        buttonLayout = QVBoxLayout()
        buttonLayout.addItem(spacerV)
        buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.correctButton)
        buttonLayout.addWidget(self.createButton)
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addItem(spacerV)

        self.mainLayout.addLayout(buttonLayout)

    def __createTextFilds(self):
        """Method that creates text areas for regex and comments"""
        lab1 = QLabel('Шаблон поиска')
        lab2 = QLabel('Комментрий')

        self.isInDBLab = QLabel('Регекс отсутствует в базе')
        self.isInDBLab.setStyleSheet('QLabel {color: green}')

        self.patternArea = QTextEdit()
        self.patternArea.setStyleSheet('QTextEdit {font-family: Segoe UI; font-size: 14pt;}')
        self.hintArea = QTextEdit()
        self.hintArea.setStyleSheet('QTextEdit {font-family: Segoe UI; font-size: 14pt;}')

        layout = QVBoxLayout()
        layout.addWidget(lab1)
        layout.addWidget(self.isInDBLab)
        layout.addWidget(self.patternArea)
        layout.addWidget(lab2)
        layout.addWidget(self.hintArea)
        self.mainLayout.addLayout(layout)

    def __createButtons(self):
        """Method that creates buttons with fast patterns for regex"""
        layout = QVBoxLayout()

        spacerV = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacerV)
        for index, value in enumerate(self.titles):
            butt = QPushButton(value)
            butt.clicked.connect(lambda x, y=self.commandsArray[index].strip('\n'): self.__takeStrings(y))
            layout.addWidget(butt)

        butt = QPushButton('Кавычки')
        butt.clicked.connect(lambda x, y='\\"\\"': self.hintArea.append(y))
        layout.addWidget(butt)

        layout.addItem(spacerV)

        self.mainLayout.addLayout(layout)

    def __takeStrings(self, mark):
        """Method that sets selected pattern for regex in the regex text area"""
        self.patternArea.insertPlainText(mark)

    def __loadData(self, categoryName):
        """Method that loads all data from DB to the container"""
        connectionData = self.__connectionToDB(categoryName)

        connectionData[1].execute('select * from {0}'.format(connectionData[2]))
        allRegex = connectionData[1].fetchall()

        connectionData[0].close()
        return allRegex

    def __uploadDataToTable(self, categoryName):
        """Method that loads and updates data in showing table on the left side of the window"""
        self.table.deleteLater()
        self.table = QTableWidget()
        self.layout2.addWidget(self.table)

        self.dataInTable = self.__loadData(categoryName)

        if len(self.dataInTable) == 0:
            QMessageBox.information(self, 'Инфо', 'База данных пустая')
            self.table.clear()
            self.isInDBLab.setText('Регекс отсутствует в базе')
            self.isInDBLab.setStyleSheet('QLabel {color: green}')
            return
        columnAmount = len(self.dataInTable[0])
        self.table.setColumnCount(columnAmount)
        self.table.setRowCount(len(self.dataInTable))
        self.table.setColumnHidden(2, True)

        # Sets first column size to content size
        # Sets second column size to remained field size
        for index in range(columnAmount):
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeToContents)

        for table_row_index, table_row in enumerate(self.dataInTable):
            for table_column_index, table_cell_value in enumerate(table_row):
                self.table.setItem(table_row_index, table_column_index, QTableWidgetItem(str(table_cell_value)))

        self.table.setHorizontalHeaderLabels(('Id', 'Шаблон', 'Комментарий'))

        # Allows to change size of the both columns
        for index in range(columnAmount):
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.Interactive)

        self.table.itemClicked.connect(lambda x, y=categoryName: self.__setDataToAreas(y))

        self.patternArea.clear()
        self.hintArea.clear()

    def __setDataToAreas(self, tableName):
        """Method that uploads data from showing table to changing areas"""
        for i in self.table.selectedItems():
            self.id = self.table.item(i.row(), 0).text()
            self.patternArea.clear()
            self.patternArea.append(self.table.item(i.row(), 1).text())

            connectionData = self.__connectionToDB(tableName)
            mysql = "select comment from {0} where id={1}".format(connectionData[2], self.id)

            connectionData[1].execute(mysql)
            comment = connectionData[1].fetchone()
            connectionData[0].close()

            self.hintArea.clear()
            self.hintArea.append(comment[0])

    def __insertDataToDB(self, tableName):
        """Method that inserts new data to DB"""
        connectionData = self.__connectionToDB(tableName)

        if self.patternArea.toPlainText() != '':
            idQuery = 'select MAX(id) from {0}'.format(connectionData[2])

            connectionData[1].execute(idQuery)
            maxId = connectionData[1].fetchone()
            connectionData[0].close()
            print(maxId)

            connectionData = self.__connectionToDB(tableName)
            mysql = 'insert into `{0}` SET `regex`="{1}", `comment` = "{3}: {2}"'.format(connectionData[2],
                                                                                    self.__shieldedSymbols()[0],
                                                                                    self.__shieldedSymbols()[1],
                                                                                    maxId[0]+1)
            connectionData[1].execute(mysql)
            connectionData[0].commit()
            connectionData[0].close()


            self.__uploadDataToTable(tableName)
            self.__cancelAction()
            rowCount = self.table.rowCount()
            self.table.setCurrentCell(rowCount - 1, 0)
        else:
            QMessageBox.information(self, 'Инфо', 'Добавьте регекс для внесения в базу данных')

    def __updateDataInRow(self, tableName):
        """Method that updates current data in DB"""
        connectionData = self.__connectionToDB(tableName)

        if self.id is not None:
            mysql = 'UPDATE `{0}` SET `regex`="{1}", `comment` ="{2}" WHERE `Id` = {3}'.format(connectionData[2],
                                                                                        self.__shieldedSymbols()[0],
                                                                                        self.__shieldedSymbols()[1],
                                                                                        self.id)
            currentRow = self.table.currentRow()
            connectionData[1].execute(mysql)
            connectionData[0].commit()
            connectionData[0].close()

            self.__uploadDataToTable(tableName)
            self.__cancelAction()
            self.table.setCurrentCell(currentRow, 0)
        else:
            QMessageBox.information(self, 'Инфо', 'Выберите строку для изменения')

    def __deleteDataFromTable(self, tableName):
        """Method that deletes current data from DB"""
        connectionData = self.__connectionToDB(tableName)

        if self.id is not None:
            dialog = QMessageBox.question(self, 'Удаление', 'Вы действительно хотите удалить запись?')
            if dialog == QMessageBox.Yes:
                mysql = "DELETE FROM `{0}` WHERE `Id` = {1}".format(connectionData[2], self.id)

                connectionData[1].execute(mysql)
                connectionData[0].commit()
                connectionData[0].close()

                self.__uploadDataToTable(tableName)
                self.__cancelAction()
        else:
            QMessageBox.information(self, 'Инфо', 'Выберите строку для удаления')

    def __cancelAction(self):
        self.patternArea.clear()
        self.hintArea.clear()
        self.id = None

    def __connectionToDB(self, tableName):
        """Method that connects to DB and return instants of connection,
        cursor and table name according to category name"""
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

    def __ifPresentInDB(self):
        """Method that checks if regex wrote in regex field is existed"""
        patternList = []

        if self.dataInTable is not None:
            for values in self.dataInTable:
                patternList.append(values[1])

        if self.dataInTable is not None:
            fromPatternArea = self.patternArea.toPlainText().replace('\\\\', '\\')
            if fromPatternArea in patternList:
                self.isInDBLab.setText('Регекс есть в базе')
                self.isInDBLab.setStyleSheet('QLabel {color: red}')
                self.createButton.setDisabled(True)
                self.createButton.setStyleSheet('QPushButton {color: red}')
                return
            else:
                self.isInDBLab.setText('Регекс отсутствует в базе')
                self.isInDBLab.setStyleSheet('QLabel {color: green}')
                self.createButton.setDisabled(False)
                self.createButton.setStyleSheet('QPushButton {color: black}')

    def __searchInTable(self, text, tableName):
        """Method that searches part of regex, that was entered, in the showing table"""
        if self.table is not None:
            foundItems = self.table.findItems(text, Qt.MatchContains)
            print(foundItems)
            print()
        else:
            return

        self.table.deleteLater()

        if len(foundItems) == 0:
            QMessageBox.information(self, 'Инфо', 'Совпадения отсутствуют')
            self.table.clear()
            self.isInDBLab.setText('Регекс отсутствует в базе')
            self.isInDBLab.setStyleSheet('QLabel {color: green}')
            self.__uploadDataToTable(tableName)
            return

        self.table = QTableWidget()
        self.layout2.addWidget(self.table)

        self.table.setColumnCount(3)
        self.table.setRowCount(len(foundItems))
        self.table.setColumnHidden(2, True)

        # Sets first column size to content size
        # Sets second column size to remained field size
        for index in range(3):
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeToContents)

        for row_index, foundItem in enumerate(foundItems):
            connect = self.__connectionToDB(tableName)
            text = str(foundItem.text())

            for i in range(3):
                column = ''

                if i == 0:
                    column = 'regex'
                else:
                    column = 'comment'

                mysqlQuery = "SELECT * FROM {0} WHERE {2}='{1}'".format(connect[2], text, column)
                connect[1].execute(mysqlQuery)
                data = connect[1].fetchone()

                if data is not None:
                    for index in range(3):
                        self.table.setItem(row_index, index, QTableWidgetItem(str(data[index])))

        connect[0].close()

        self.table.setHorizontalHeaderLabels(('Id', 'Шаблон', 'Комментарий'))

        # Allows to change size of the both columns
        for index in range(3):
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.Interactive)

        self.table.itemClicked.connect(lambda x, y=tableName: self.__setDataToAreas(y))

        self.patternArea.clear()
        self.hintArea.clear()

    def __searchForCoincidence(self, text, tableName):
        connection = self.__connectionToDB(tableName)
        self.table.deleteLater()

        data = []

        for i in range(2):
            column = ''

            if i == 0:
                column = 'regex'
            else:
                column = 'comment'

            mysql = "select * from {0} where {2} like '%{1}%'".format(connection[2], text, column)
            connection[1].execute(mysql)
            data.extend(connection[1].fetchall())

        connection[0].close()

        if len(data) == 0:
            QMessageBox.information(self, 'Инфо', 'Совпадения отсутствуют')
            self.table.clear()
            self.isInDBLab.setText('Регекс отсутствует в базе')
            self.isInDBLab.setStyleSheet('QLabel {color: green}')
            self.__uploadDataToTable(tableName)
            return

        self.table = QTableWidget()
        self.layout2.addWidget(self.table)

        self.table.setColumnCount(3)
        self.table.setRowCount(len(data))
        self.table.setColumnHidden(2, True)

        # Sets first column size to content size
        # Sets second column size to remained field size
        for index in range(3):
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.ResizeToContents)

        self.table.setHorizontalHeaderLabels(('Id', 'Шаблон', 'Комментарий'))

        # Allows to change size of the both columns
        for index in range(3):
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.Interactive)

        for row_index, row_value in enumerate(data):
            for column_index in range(len(row_value)):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(row_value[column_index])))

        self.table.itemClicked.connect(lambda x, y=tableName: self.__setDataToAreas(y))

        self.patternArea.clear()
        self.hintArea.clear()

    def __shieldedSymbols(self):
        """Method that shields symbols in text"""
        pattern = self.patternArea.toPlainText().replace('\\', '\\\\')
        hint = self.hintArea.toPlainText().replace('\\', '\\\\')
        pattern = pattern.replace("'", '\'')
        hint = hint.replace("'", '\'')
        return pattern, hint
