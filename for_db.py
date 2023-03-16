import sqlite3


def createBD():  # инициализация класса
    con = sqlite3.connect('database.db', check_same_thread=False)  # подключение БД
    create_table1 = """CREATE TABLE IF NOT EXISTS assortment (
    id    INTEGER    PRIMARY KEY AUTOINCREMENT,
    name        STRING  NOT NULL,
    http        STRING,
    description STRING,
    category    INT     REFERENCES category (id) 
);

"""
    create_table2 = """CREATE TABLE IF NOT EXISTS discounts (
     id  INTEGER   PRIMARY KEY AUTOINCREMENT,
    name   STRING  NOT NULL,
    des_if STRING
);


"""
    create_table3 = """CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
     id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   STRING  NOT NULL,
    status BOOLEAN NOT NULL,
    id_tg  INTEGER NOT NULL
                   UNIQUE,
    username STRING
);
"""
    create_table6 = """CREATE TABLE IF NOT EXISTS category ( id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING, 
    http STRING
);
        """
    con.cursor().execute(create_table1)  # создание отсутствующих и необходимых таблиц
    con.cursor().execute(create_table2)
    con.cursor().execute(create_table3)
    con.cursor().execute(create_table4)
    con.cursor().execute(create_table5)
    con.cursor().execute(create_table6)
    con.commit()


def get_answer(self, key_words):
    # self.con.cursor().execute('''SELECT FROM ''')
    return


def add_que_ans(con, question, answer):
    con.cursor().execute(f'''INSERT INTO question_answer(key_words, answer)
             VALUES ({question}, {answer})''')
    con.commit()


def get_assort(con):
    return con.cursor().execute('''SELECT * FROM category''').fetchall()


def get_category_assort(con, id_category):
    return con.cursor().execute(f'''SELECT id, name, description, http
          FROM assortment WHERE category = "{id_category}"''').fetchall()


def add_category(con, name, http):
    con.cursor().execute(f'''INSERT INTO category(name, http)
                         VALUES('{name}', '{http}')''')
    con.commit()


def del_category(con, name):
    if not is_category(con, name):
        return False
    con.cursor().execute(f'''DELETE from category WHERE name = "{name}"''')
    con.commit()
    return True


def is_category(con, name):
    return len(con.cursor().execute(f'''SELECT * FROM category WHERE name="{name}"''').fetchall()) != 0


def is_assort(con, name):
    return len(con.cursor().execute(f'''SELECT * FROM assortment WHERE name="{name}"''').fetchall()) != 0


def add_assort(con, name, opisanie, http, category):
    con.con.cursor().execute(f'''INSERT INTO assortment(name, http, description, category)
                                 VALUES('{name}', '{http}', '{opisanie}, '{category}')''')
    con.commit()


def del_assort(con, name):
    if not is_category(con, name):
        return False
    con.cursor().execute(f'''DELETE from assortment WHERE name = "{name}"''')
    con.commit()
    return True


def del_que_ans(con, question):
    con.cursor().execute(f'''DELETE from question_answer WHERE key_words = "{question}"''')
    con.commit()


def remove_answer(con, question, answer):
    con.cursor().execute(f'''UPDATE question_answer
            SET answer = '{answer}' WHERE key_words = "{question}"''')
    con.commit()


def add_user(con, id_tg, name, username):
    con.cursor().execute(f'''INSERT INTO users(name, status, id_tg, username)
                                 VALUES('{name}', False, "{id_tg}", "{username}")''')
    con.commit()


def remove_status(con, name):
    con.cursor().execute(f'''UPDATE users
                    SET status = True WHERE name = "{name}"''')
    con.commit()


def get_discount(con):
    return con.cursor().execute('''SELECT * FROM discounts''').fetchall()


def add_discount(con, name, des):
    con.cursor().execute(f'''INSERT INTO discounts(name, des_if)
                                         VALUES('{name}', "{des}")''')
    con.commit()


def remove_discount(con, name, des):
    con.cursor().execute(f'''UPDATE discounts
                            SET des_if="{des}" WHERE name = "{name}"''')
    con.commit()


def del_discount(con, name):
    con.cursor().execute(f'''DELETE from discounts WHERE name = "{name}"''')
    con.commit()


def get_notification(con):
    return con.cursor().execute('''SELECT * FROM notifications''').fetchall()


def add_notification(con, text, time):
    con.cursor().execute(f'''INSERT INTO notifications(text, time)
                                         VALUES("{text}", "{time}")''')
    con.commit()


def remove_notification(con, text, time):
    con.cursor().execute(f'''UPDATE notifications
                            SET  time ="{time}" WHERE text="{text}"''')
    con.commit()


def del_notification(con, text):
    con.cursor().execute(f'''DELETE from notifications WHERE  text = "{text}"''')
    con.commit()


def get_info_for_base(con):
    itog = []
    users = 'Пользователи', [
        ('ID', 'ФИО', 'Статус', 'Должность(1-админ, 0-клиент', 'ID TG', 'UserName')] + con.cursor().execute(f'''SELECT name, 
            status, id_tg, username FROM Users''').fetchall()
    itog.append(users)
    categories = 'Категории', [
        ('ID Категории', 'Название категории', 'Путь к файлу картинки')] + \
                 con.cursor().execute(f'''SELECT id, name, http FROM category''').fetchall()
    itog.append(categories)
    mailings = 'Уведомления', [
        ('Сообщение', 'Дата отправления', 'Для сотрудников компании...')] + \
               con.cursor().execute(f'''SELECT text, date,
        company FROM Mailings''').fetchall()
    itog.append(mailings)
    questions = 'Вопросы', [
        ('Вопрос', 'Ответ', 'Для сотрудников компании...')] + \
                con.cursor().execute(f'''SELECT text_q, text_a,
        company FROM Questions''').fetchall()
    itog.append(questions)
    return itog



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
# con.add_notification('12', '122')
# print(con.get_notification())
# con.remove_notification('12', '98')
# con.del_notification('12')
