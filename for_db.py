import sqlite3


class Control:
    def __init__(self):  # инициализация класса
        self.con = sqlite3.connect('database.db', check_same_thread=False)  # подключение БД
        create_table1 = """CREATE TABLE IF NOT EXISTS assortment (
    id        PRIMARY KEY AUTOINCREMENT,
    name        STRING  NOT NULL,
    http        STRING,
    description STRING,
    category    INT     REFERENCES category (id) 
);

"""
        create_table2 = """CREATE TABLE IF NOT EXISTS discounts (
     id     PRIMARY KEY AUTOINCREMENT,
    name   STRING  NOT NULL,
    des_if STRING
);


"""
        create_table3 = """CREATE TABLE IF NOT EXISTS notifications (
    id           PRIMARY KEY AUTOINCREMENT,
    text    TEXT,
    time
);
"""
        create_table4 = """CREATE TABLE IF NOT EXISTS question_answer (
    key_words STRING NOT NULL,
    answer           NOT NULL
);
"""
        create_table5 = """CREATE TABLE IF NOT EXISTS users (
    id      PRIMARY KEY AUTOINCREMENT,
    name   STRING  NOT NULL,
    status BOOLEAN NOT NULL
);
"""
        create_table6 = """CREATE TABLE IF NOT EXISTS category ( id  PRIMARY KEY AUTOINCREMENT,
    name STRING, 
    http STRING
);
        """
        self.con.cursor().execute(create_table1)  # создание отсутствующих и необходимых таблиц
        self.con.cursor().execute(create_table2)
        self.con.cursor().execute(create_table3)
        self.con.cursor().execute(create_table4)
        self.con.cursor().execute(create_table5)
        self.con.cursor().execute(create_table6)
        self.con.commit()

    def get_answer(self, key_words):
        #self.con.cursor().execute('''SELECT FROM ''')
        return

    def add_que_ans(self, question, answer):
        self.con.cursor().execute(f'''INSERT INTO question_answer(key_words, answer)
                 VALUES ({question}, {answer})''')
        self.con.commit()

    def get_assort(self):
        return self.con.cursor().execute('''SELECT * FROM category''').fetchall()

    def get_category_assort(self, id_category):
        return self.con.cursor().execute(f'''SELECT id, name, description, http
          FROM assortment WHERE category = "{id_category}"''').fetchall()

    def add_category(self, name, http):
        self.con.cursor().execute(f'''INSERT INTO category(name, http)
                         VALUES('{name}', '{http}')''')
        self.con.commit()

    def del_category(self, name):
        if not self.is_category(name):
            return False
        self.con.cursor().execute(f'''DELETE from category WHERE name = "{name}"''')
        self.con.commit()
        return True

    def is_category(self, name):
        return len(self.con.cursor().execute(f'''SELECT * FROM category WHERE name="{name}"''').fetchall()) != 0

    def is_assort(self, name):
        return len(self.con.cursor().execute(f'''SELECT * FROM assortment WHERE name="{name}"''').fetchall()) != 0

    def add_assort(self, name, opisanie, http, category):
        self.con.cursor().execute(f'''INSERT INTO assortment(name, http, description, category)
                                 VALUES('{name}', '{http}', '{opisanie}, '{category}')''')
        self.con.commit()

    def del_assort(self, name):
        if not self.is_category(name):
            return False
        self.con.cursor().execute(f'''DELETE from assortment WHERE name = "{name}"''')
        self.con.commit()
        return True

    def del_que_ans(self, question):
        self.con.cursor().execute(f'''DELETE from question_answer WHERE key_words = "{question}"''')
        self.con.commit()

    def remove_answer(self, question, answer):
        self.con.cursor().execute(f'''UPDATE question_answer
            SET answer = '{answer}' WHERE key_words = "{question}"''')
        self.con.commit()

    def add_user(self, name):
        self.con.cursor().execute(f'''INSERT INTO users(name, status)
                                 VALUES('{name}', False)''')
        self.con.commit()

    def remove_status(self, name):
        self.con.cursor().execute(f'''UPDATE users
                    SET status = True WHERE name = "{name}"''')
        self.con.commit()

    def get_discount(self):
        return self.con.cursor().execute('''SELECT * FROM discounts''').fetchall()

    def add_discount(self, name, des):
        self.con.cursor().execute(f'''INSERT INTO discounts(name, des_if)
                                         VALUES('{name}', "{des}")''')
        self.con.commit()

    def remove_discount(self, name, des):
        self.con.cursor().execute(f'''UPDATE discounts
                            SET des_if="{des}" WHERE name = "{name}"''')
        self.con.commit()

    def del_discount(self, name):
        self.con.cursor().execute(f'''DELETE from discounts WHERE name = "{name}"''')
        self.con.commit()

    def get_notification(self):
        return self.con.cursor().execute('''SELECT * FROM notifications''').fetchall()

    def add_notification(self, text, time):
        self.con.cursor().execute(f'''INSERT INTO notifications(text, time)
                                         VALUES("{text}", "{time}")''')
        self.con.commit()

    def remove_notification(self, text, time):
        self.con.cursor().execute(f'''UPDATE notifications
                            SET " time ="{time}" WHERE text="{text}''')
        self.con.commit()

    def del_notification(self, text):
        self.con.cursor().execute(f'''DELETE from notifications WHERE  text = "{text}"''')
        self.con.commit()



con = Control()
# con.add_que_ans('12', '34')
# print(con.get_assort())
# print(con.get_category_assort(0))
# con.add_category('name', 'ooo')
# con.del_category('Мужское')
# print(con.is_category('12'))
# print(con.is_assort('12'))
# con.del_assort('12')
# con.del_que_ans('12')
# con.remove_answer('12', '78')
# con.add_user('1233')
# con.remove_status('12')
# con.add_discount('12', '23')
# print(con.get_discount())
# con.remove_discount('12', '56')
# con.del_discount('12')
con.add_notification('12', '122')
