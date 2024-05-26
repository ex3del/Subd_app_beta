import sqlite3 as sq
region = 'Дальневосточный'
fio = ''
city = ''
grnti = ''
key_words= ''
take_part= ''
date= ''
rubrika= ''
oblname= ''
conn = sq.connect('default_database.db')
cursor = conn.cursor()
cursor.execute(f"SELECT kod FROM ma_tab WHERE (region = '{region}' OR '{region}' IS NULL) AND (city = '{city}' OR '{city}' IS NULL) AND (grnti = '{grnti}' OR '{grnti}' IS NULL) AND (key_words = '{key_words}' OR '{key_words}' IS NULL) AND (take_part = '{take_part}' OR '{take_part}' IS NULL) AND (input_date = '{date}' OR '{date}' IS NULL) AND (rubrika = '{rubrika}' OR '{rubrika}' IS NULL) AND (oblname = '{oblname}' OR '{oblname}' IS NULL);")
kods = cursor.fetchone()
print(kods)