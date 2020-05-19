import threading
import sqlite3
import data

global db, sql, lock
db = sqlite3.connect('data-emotions.db', check_same_thread=False)
sql = db.cursor()
lock = threading.Lock()


def create():
    lock.acquire(True)

    sql.execute("""CREATE TABLE IF NOT EXISTS diary (
            key_ INTEGER PRIMARY KEY,
            id INTEGER,
            situation TEXT,
            emotion TEXT,
            days INTEGER
            )""")
    db.commit()
    lock.release()


def new_emotion(user_id, emotion, islock=True):
    if islock:
        lock.acquire(True)

    sql.execute(f'INSERT INTO diary (id, situation, emotion, days) VALUES (?, ?, ?, ?)',
                (user_id, None, emotion, data.get_days(user_id, False)))
    db.commit()
    if islock:
        lock.release()


def situation(user_id, text, islock=True):
    lock.acquire(True)
    text = str(text)
    number = get_max_key(user_id)
    print(number)
    sql.execute(f'UPDATE diary SET situation = "{text}" WHERE key_ = {number}')
    db.commit()
    sql.execute(f'SELECT * FROM diary')
    f = sql.fetchone()
    print('emo', f)

    lock.release()


def get_week_diary(user_id, islock=True):
    if islock:
        lock.acquire(True)
    days = data.get_days(user_id, False)
    print('true')
    res = []
    if days < 8:
        start = 1
    else:
        start = data.get_days(user_id) - 7
    end = days
    for i in range(start, end + 1):
        sql.execute(f"SELECT situation FROM diary WHERE id = {user_id} AND days = {i}")
        situations = sql.fetchall()
        part = [what_day(i)]

        for sit in situations:
            print(sit)
            sql.execute(f"SELECT emotion FROM diary WHERE id = {user_id} AND situation = '{sit[0]}'")
            emotion = sql.fetchone()
            print(emotion)
            emo = [(emotion[0], sit[0])]
            print(emo)
            part.append(emo)
            print('кортеж', part)
        res.append(part)
    if islock:
        lock.release()
    return res


# функция со всем дневником
def get_diary(user_id, islock=True):
    pass


def what_day(i):
    return ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'][i]


def get_max_key(user_id):
    sql.execute(f"SELECT * FROM diary")
    f = sql.fetchall()
    print(f)
    f.reverse()
    print(f)
    for i in range(len(f)):
        if f[i][1] == user_id:
            print(i)
            return i + 1
