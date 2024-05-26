from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QAbstractItemView
from main_form import Ui_MainWindow
import sys
from connection import Data
from PyQt6.QtSql import QSqlTableModel
from add_string import Ui_Dialog
from table_view import SqlTableModel
import re
import sqlite3 as sq
class zadanie(QMainWindow):
    def __init__(self):
        super(zadanie, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = Data()
        self.view_data()

        self.ui.btn_add_string.clicked.connect(self.open_new_string_window)
        self.ui.btn_edit_string.clicked.connect(self.open_new_string_window)
        self.ui.btn_delete_string.clicked.connect(self.delete_current_string)
        self.ui.filter.clicked.connect(self.setup_filter)
        self.ui.defilt.clicked.connect(self.reset_filter)
        self.ui.ngrup.clicked.connect(self.make_group)



    def view_data(self, kod=None):
        self.model = SqlTableModel()
        self.model.setTable('ma_tab')
        self.model.select()
        self.model.set_header()
        if kod:
            self.model.setFilter(f"kod IN {tuple(kod)}")
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setSortingEnabled(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)

    def view_data_grp(self, kod=None):
        self.model = SqlTableModel()
        self.model.setTable('ma_tab')
        self.model.select()
        self.model.set_header()
        if kod:
            self.model.setFilter(f"kod IN {tuple(kod)}")
        self.ui.grp_tab.setModel(self.model)
        self.ui.grp_tab.setSortingEnabled(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)

    def open_new_string_window(self):
        sender = self.sender()

        if sender.text() == 'Добавление записи':
            self.new_window = QtWidgets.QDialog()
            self.ui_window = Ui_Dialog()
            self.ui_window.setupUi(self.new_window)
            self.new_window.show()
            self.ui_window.btn_add_string.clicked.connect(self.add_new_string)



        else:
            # Получаем индекс выбранной строки в таблице
            try:
                index = self.ui.tableView.selectedIndexes()[0]
                # Получаем значения остальных столбцов выбранной строки
                fio = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 1)))
                region = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 2)))
                city = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 3)))
                grnti = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 4)))
                key_words = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 5)))
                take_part = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 6)))
                date = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 7)))
                rubrika = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 8)))
                oblname = str(self.ui.tableView.model().data(self.ui.tableView.model().index(index.row(), 9)))
            except IndexError: return


            self.new_window = QtWidgets.QDialog()
            self.ui_window = Ui_Dialog()
            self.ui_window.setupUi(self.new_window)
            self.ui_window.le_fio.setText(fio)
            self.ui_window.cb_region.setCurrentText(region)
            self.ui_window.le_gorod.setText(city)
            self.ui_window.le_grnti.setText(grnti)
            self.ui_window.le_keywords.setText(key_words)
            self.ui_window.le_takepart.setText(take_part)
            self.ui_window.date.setDate(QDate.fromString(date, "yyyy-MM-dd"))
            #self.ui_window.cb_rubrika.setCurrentText(rubrika)
            self.ui_window.cb_oblast.setCurrentText(oblname)
            self.new_window.show()
            self.ui_window.btn_add_string.clicked.connect(self.edit_current_string)

    def grnti_to_rub(self, grnti):
        global rubrika
        conn = sq.connect('default_database.db')
        cursor = conn.cursor()

        if len(grnti) < 2:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Номер ГРНТИ не существует")
            return

        if ';' in grnti:
            grnti1, grnti2 = grnti.split(';')[0][:2], grnti.split(';')[1][:2]
            cursor.execute("SELECT field2 FROM grntirub WHERE field1=?", (grnti1,))
            result = list(cursor.fetchone())
            cursor.execute("SELECT field2 FROM grntirub WHERE field1=?", (grnti2,))
            result.append(cursor.fetchone()[0])

        else:
            cursor.execute("SELECT field2 FROM grntirub WHERE field1=?", (grnti[:2],))
            result = cursor.fetchone()


        if len(result) < 2:
            subject = result[0]

        elif len(result) == 2:
            subject = '; '.join(result)

        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Несуществующий номер ГРНТИ. Введите значение заново.")
            return

        return subject
    def add_new_string(self):

        #name, region, city, grnti, key_words, take_part, input_date, rubrika, oblname
        fio = self.ui_window.le_fio.text()
        region = self.ui_window.cb_region.currentText()
        city = self.ui_window.le_gorod.text()
        grnti = self.ui_window.le_grnti.text()
        key_words = self.ui_window.le_keywords.text()
        take_part = self.ui_window.le_takepart.text()
        date = self.ui_window.date.text()
        #rubrika = self.ui_window.cb_rubrika.currentText()
        rubrika = self.grnti_to_rub(grnti)
        oblname = self.ui_window.cb_oblast.currentText()



        if not fio:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректное ФИО")
            return
        if not city or not city.isalpha():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректный город")
            return

        if not grnti or not re.match("^[0-9.;]+$", grnti):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Номер ГРНТИ должен состоять только из цифр")
            return

        self.conn.add_new_string_query(date, fio, city, grnti, key_words, oblname, region, rubrika, take_part)
        self.view_data()
        self.new_window.close()


    def edit_current_string(self):
        index = self.ui.tableView.selectedIndexes()[0]
        id = str(self.ui.tableView.model().data(index))
        fio = self.ui_window.le_fio.text()
        region = self.ui_window.cb_region.currentText()
        city = self.ui_window.le_gorod.text()
        grnti = self.ui_window.le_grnti.text()
        key_words = self.ui_window.le_keywords.text()
        take_part = self.ui_window.le_takepart.text()
        date = self.ui_window.date.text()
        #rubrika = self.ui_window.cb_rubrika.currentText()
        rubrika = self.grnti_to_rub(grnti)
        oblname = self.ui_window.cb_oblast.currentText()

        if not fio:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректное ФИО")
            return
        if not city or not city.isalpha():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректный город")
            return

        if not grnti or not re.match("^[0-9.;]+$", grnti):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Номер ГРНТИ должен состоять только из цифр. Два номера должна разделять ';'")
            return

        self.conn.update_string_query(date, fio, city, grnti, key_words, oblname, region, rubrika, take_part, id)
        self.view_data()
        self.new_window.close()


    def delete_current_string(self):
        index = self.ui.tableView.selectedIndexes()[0]
        id = str(self.ui.tableView.model().data(index))

        self.conn.delete_string_query(id)
        self.view_data()

    def reset_filter(self):
        pass

    def setup_filter(self):

        # name, region, city, grnti, key_words, take_part, input_date, rubrika, oblname
        region = self.ui.reg_fil.currentText()
        city = self.ui.city_fil.text()
        grnti = self.ui.grnti_fil.text()
        key_words = self.ui.keywr_fil.text()
        take_part = self.ui.mark_fil.text()
        date = self.ui.date_fil.text()
        rubrika = self.ui.rubr_fil.currentText()
        oblname = self.ui.obl_fil.currentText()
        date = date.split('.')
        date = '-'.join([date[2], date[0], date[1]])
        conn = sq.connect('default_database.db')
        cursor = conn.cursor()
        grnti = grnti[:2]

        if region:
            cursor.execute(f"SELECT kod FROM ma_tab WHERE region='{region}'")
            res = cursor.fetchall()
            if res:
                regions = set([[int(x) for x in i][0] for i in res])
            else: regions = {9999}
        else: regions = {0}


        if city:
            cursor.execute("SELECT kod FROM ma_tab WHERE city=?", (city.capitalize(),))
            res = cursor.fetchall()
            if res:
                citites = set([[int(x) for x in i][0] for i in res])
            else:
                citites = {9999}
        else: citites = {0}
        #print(citites,2)

        if grnti:
            cursor.execute("SELECT kod FROM ma_tab WHERE SUBSTRING(grnti, 1, 2)=?", (grnti,))
            res = cursor.fetchall()
            if res:
                grntis = set([[int(x) for x in i][0] for i in res])
            else:
                grntis = {9999}
        else: grntis = {0}
        #print(grntis,3)

        if key_words:
            cursor.execute("SELECT kod FROM ma_tab WHERE key_words=?", (key_words,))
            res = cursor.fetchall()
            if res:
                kwrds = set([[int(x) for x in i][0] for i in res])
            else:
                kwrds = {9999}
        else: kwrds = {0}
        #print(kwrds,4)

        if take_part:
            cursor.execute("SELECT kod FROM ma_tab WHERE take_part=?", (take_part,))
            res = cursor.fetchall()
            if res:
                tkprt = set([[int(x) for x in i][0] for i in res])
            else:
                tkprt = {9999}
        else: tkprt = {0}
        #print(tkprt,5)


        if date != '2023-07-01':
            cursor.execute("SELECT kod FROM ma_tab WHERE input_date=?", (date,))
            res = cursor.fetchall()
            if res:
                dates = set([[int(x) for x in i][0] for i in res])
            else:
                dates = {9999}
        else: dates = {0}
        #print(dates,6)

        if rubrika:
            cursor.execute("SELECT kod FROM ma_tab WHERE rubrika LIKE '%{}%'".format(rubrika))
            res = cursor.fetchall()
            if res:
                rubs = set([[int(x) for x in i][0] for i in res])
            else:
                rubs = {9999}
        else: rubs = {0}
        #print(rubs,7)

        if oblname:
            cursor.execute("SELECT kod FROM ma_tab WHERE oblname=?", (oblname,))
            res = cursor.fetchall()
            if res:
                obs = set([[int(x) for x in i][0] for i in res])
            else:
                obs = {9999}
        else: obs = {0}
        #print(obs,8)

        kods = {i for i in range(9999)}
        for i in [citites, grntis, kwrds, tkprt, dates, rubs, regions, obs]:
            if 0 not in i:
                kods = kods.intersection(i)
            else: pass
            if 9999 in i:
                kods = {}
                break

        
        if len(kods) != 0:
            self.view_data(kods)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет удовлетворяющих значений")
            return

    def reset_filter(self):
        self.ui.reg_fil.setCurrentIndex(0)
        self.ui.city_fil.clear()
        self.ui.grnti_fil.clear()
        self.ui.keywr_fil.clear()
        self.ui.mark_fil.clear()
        self.ui.date_fil.clear()
        self.ui.rubr_fil.setCurrentIndex(0)
        self.ui.obl_fil.setCurrentIndex(0)
        self.view_data()

    def make_group(self):
        index = self.ui.tableView.selectedIndexes()
        k = 0
        indexes = []
        for i in index:
            if k % 10 == 0:
                id = str(self.ui.tableView.model().data(i))
                indexes.append(id)
            k += 1
        self.view_data_grp(indexes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = zadanie()
    window.show()

    sys.exit(app.exec())




