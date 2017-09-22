import pymysql as mdb
import shelve
from PyQt5.QtWidgets import QMessageBox


class DBConnector:
    def __init__(self, mainWindow):
        self.__connection = None
        self.__cursor = None
        self.mainWindow = mainWindow

    def getConnection(self, isFirst=False):
        with shelve.open('db_setup') as f:
            try:
                if isFirst:
                    self.__connection = mdb.connect(f['host'], f['name'], f['password'], charset="utf8")
                else:
                    self.__connection = mdb.connect(f['host'], f['name'], f['password'], f['db'], charset="utf8")
            except mdb.err.OperationalError:
                QMessageBox.information(self.mainWindow, 'Инфо',
                                        'Нет подключения к базе.\nПроверьте установлена и запущена ли база')
                self.__connection = None
        return self.__connection

    def getCursorExecute(self, mysqlQuery):
        if self.__connection is not None:
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(mysqlQuery)

        return self.__cursor

    def getTableName(self, tableName):
        with open('categories', encoding='utf-8') as f:
            for value in f:
                tableNameIns = value.split(';')
                if tableNameIns[0] == tableName:
                    nameForTableLoad = tableNameIns[1].strip(' \n')

        return nameForTableLoad

    def closeConnection(self):
        if self.__connection is not None:
            self.__connection.close()

    def commit(self):
        if self.__connection is not None:
            self.__connection.commit()
