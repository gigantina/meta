import threading
import sqlite3

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


def new(user_id):
    lock.acquire(True)
    sql.execute("SELECT id FROM diary")
    if not sql.fetchone():
        sql.execute(f"INSERT INTO diary VALUES (?, ?, ?, ?)",
                    (user_id, None, None, 1))
        db.commit()
    lock.release()


def get_days(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT days FROM diary WHERE id = {user_id}")
    res = sql.fetchone()
    print(res)
    if islock:
        lock.release()
    return res[0]


def new_emotion(user_id, emotion, islock=True):
    if islock:
        lock.acquire(True)

    sql.execute(f'INSERT INTO diary (id, situation, emotion, days) VALUES (?, ?, ?, ?)',
                (user_id, None, emotion, get_days(user_id, False)))
    if islock:
        lock.release()


def situation(user_id, text, islock=True):
    lock.acquire(True)
    text = str(text)
    sql.execute(f'UPDATE diary SET situation = {text} WHERE key_ = {get_max_key()}')
    f = sql.fetchone()
    print('emo', f)
    db.commit()
    lock.release()


def get_week_diary(user_id, islock=True):
    if islock:
        lock.acquire(True)
    days = get_days(user_id, False)
    print('true')
    res = []
    if days < 8:
        start = 1
    else:
        start = get_days(user_id) - 7
    end = days
    for i in range(start, end + 1):
        sql.execute(f"SELECT situation FROM diary WHERE id = {user_id} AND days = {i}")
        situations = sql.fetchall()
        tuple_ = (what_day(i),)

        for sit in situations:
            print(sit)
            sql.execute(f"SELECT emotion FROM diary WHERE id = {user_id} AND situation = '{sit[0]}'")
            emotion = sql.fetchone()
            print(emotion)
            part = (emotion, sit)
            tuple_ += part
            print('кортеж', tuple_)
        res.append(tuple_)
    if islock:
        lock.release()
    return res


# функция со всем дневником
def get_diary(user_id, islock=True):
    pass


def what_day(i):
    return ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'][i]


def new_day(user_id, islock=True):
    lock.acquire(True)
    sql.execute(f"UPDATE diary SET days = days + 1 WHERE key_ = {get_max_key()}")
    db.commit()
    lock.release()


def get_max_key():
    sql.execute(f"SELECT * FROM diary")
    f = sql.fetchall()
    return f[-1][0]
