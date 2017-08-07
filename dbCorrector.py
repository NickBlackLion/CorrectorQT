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
                              '\\s', '\\w+', '{2}', '|', '.', '[0-9]', '\.', '\\b', '\\b|\\b']

        self.__createTable()
        self.__createTextFilds()
        self.__createButtons()

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

    # TODO добавить функции CRUD под нажатие кнопок
    def __createTextFilds(self):
        lab1 = QLabel('Шаблон поиска')
        lab2 = QLabel('Комментрий')

        self.patternArea = QTextEdit()
        self.hintArea = QTextEdit()

        self.createButton = QPushButton('Добавить')
        # self.correctButton.clicked.connect(lambda: self.__updateDataInDB())
        self.correctButton = QPushButton('Редактировать')
        # self.correctButton.clicked.connect(lambda: self.__updateDataInDB())
        self.deleteButton = QPushButton('Удалить')
        # self.deleteButton.clicked.connect(lambda: self.__deleteFromDB())
        self.cancelButton = QPushButton('Отменить')
        # self.deleteButton.clicked.connect(lambda: self.__deleteFromDB())

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
        print('__takeStrings')
        self.patternArea.insertPlainText(mark)

    def __loadData(self, categoryName):
        allRegex = None

        con = None

        with shelve.open('db_setup') as f:
            con = mdb.connect(f['host'], f['name'], f['password'], f['db'], charset="utf8")

        with con:
            cur = con.cursor()
            nameForTableLoad = None

            with open('categories', encoding='utf-8') as f:
                for value in f:
                    tableNameIns = value.split(';')
                    if tableNameIns[0] == categoryName:
                        nameForTableLoad = tableNameIns[1].strip(' \n')

            if nameForTableLoad is not None:
                cur.execute('select * from {0}'.format(nameForTableLoad))
                allRegex = cur.fetchall()

        return allRegex

    def __uploadDataToTable(self, categoryName):
        data = self.__loadData(categoryName)

        if len(data) == 0:
            QMessageBox.information(self, 'Инфо', 'База данных пустая')
            return

        self.table.setColumnCount(len(data[0]))
        self.table.setRowCount(len(data))

        for table_row_index, table_row in enumerate(data):
            for table_column_index, table_cell_value in enumerate(table_row):
                self.table.setItem(table_row_index, table_column_index, QTableWidgetItem(str(table_cell_value)))

        self.table.setHorizontalHeaderLabels(('Id', 'Шаблон', 'Комментарий'))
        self.table.itemClicked.connect(lambda: self.__setDataToAreas())

    def __setDataToAreas(self):
        for i in self.table.selectedItems():
            if i.column() == 0:
                self.patternArea.clear()
                self.patternArea.append(self.table.item(i.row(), (i.column()+1)).text())
                self.hintArea.clear()
                self.hintArea.append(self.table.item(i.row(), (i.column()+2)).text())
