from PyQt6 import QtWidgets, QtSql

class Data:
    def __init__(self):
        super(Data, self).__init__()
        self.create_connection()

    def create_connection(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('default_database.db')

        """if not db.open():
            QtWidgets.QMessageBox.critical(None, 'Невозможно октрыть базу данных',
                                           "Нажмите для выхода", QtWidgets.QMessageBox.Cancel)
            return False
        query = QtSql.QSqlQuery()
        query.exec()
        return True"""

    def execute_query_with_params(self, sql_query, query_values=None):
        query = QtSql.QSqlQuery()
        query.prepare(sql_query)

        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()

        return query

    def add_new_string_query(self, date, fio, gorod, grnti, keywords, oblast, region, rubrika, takepart):
        sql_query = "INSERT INTO ma_tab (name, region, city, grnti, key_words, take_part, input_date, rubrika, oblname) VALUES (?,?,?,?,?,?,?,?,?)"
        self.execute_query_with_params(sql_query, [fio, region, gorod, grnti, keywords, takepart, date, rubrika, oblast])

    def update_string_query(self, date, fio, gorod, grnti, keywords, oblast, region, rubrika, takepart, id):
        sql_query = "UPDATE ma_tab SET name=?, region=?, city=?, grnti=?, key_words=?, take_part=?, input_date=?, rubrika=?, oblname=? WHERE kod=?"
        self.execute_query_with_params(sql_query, [fio, region, gorod, grnti, keywords, takepart, date, rubrika, oblast, id])

    def delete_string_query(self, id):
        sql_query = 'DELETE FROM ma_tab WHERE kod=?'
        self.execute_query_with_params(sql_query, [id])



