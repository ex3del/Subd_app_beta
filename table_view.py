from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel



class SqlTableModel(QSqlTableModel):

    COLUMNS_DICT = {
                'kod': 'Код',
                'name': 'ФИО',
                'region': 'Регион',
                'city': 'Город',
                'grnti': 'ГРНТИ',
                'key_words': 'Ключевые слова',
                'take_part': 'Метка',
                'input_date': 'Дата занесения',
                'rubrika': 'Сфера интересов',
                'oblname': 'Область',
    }


    def __init__(self):
        super(SqlTableModel, self).__init__()
        self.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)

    def set_header(self):
        for i in range(self.columnCount()):
            header_data = self.headerData(i, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
            column_name = self.COLUMNS_DICT[header_data]

            self.setHeaderData(i, Qt.Orientation.Horizontal, column_name, Qt.ItemDataRole.DisplayRole)
            self.setHeaderData(i, Qt.Orientation.Horizontal, header_data, Qt.ItemDataRole.UserRole)
