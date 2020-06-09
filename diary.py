import threading
import sqlite3
import data
import functions as f

global db, sql, lock
db = sqlite3.connect('data-emotions.db', check_same_thread=False)
sql = db.cursor()
lock = threading.Lock()


def new_emotion(user_id, emotion, islock=True):  # новая запись в дневник
    if islock:
        lock.acquire(True)

    sql.execute("INSERT INTO diary (id, situation, emotion, days, days_of_week) VALUES (?, ?, ?, ?, ?)",
                (user_id, None, emotion, data.get_days(user_id), f.day(user_id)))
    db.commit()
    if islock:
        lock.release()


def situation(user_id, text, islock=True):  # дополнение записи ситуацией, описывающей эмоцию
    if islock:
        lock.acquire(True)
    text = str(text)
    number = get_max_key(user_id)
    sql.execute(f'UPDATE diary SET situation = "{text}" WHERE key_ = {number}')
    db.commit()
    data.situation(user_id, 0, False)
    if islock:
        lock.release()


# функция, возвращающая записи в дневнике за неделю
def get_week_diary(user_id, islock=True):
    days = data.get_days(user_id)
    if days < 8:
        start = 1
    else:
        start = data.get_days(user_id) - 7
    end = days
    return (start, end)


def get_notes(start, end, user_id, islock=True):
    if islock:
        lock.acquire(True)
    res = []
    for i in range(start, end + 1):
        sql.execute(f"SELECT situation FROM diary WHERE id = {user_id} AND days = {i}")
        situations = sql.fetchall()
        sql.execute(f"SELECT days_of_week FROM diary WHERE id = {user_id} AND days = {i}")
        day = sql.fetchone()
        part = []
        if day:
            part.append(what_day(day[0]))
        else:
            part.append(None)

        for sit in situations:
            sql.execute(f"SELECT emotion FROM diary WHERE id = {user_id} AND situation = '{sit[0]}'")
            emotion = sql.fetchone()
            emo = [(emotion[0], sit[0])]
            part.append(emo)
        res.append(part)
    if islock:
        lock.release()
    return res


# функция, возвращающая записи в дневнике за все время
def get_all_diary(user_id, islock=True):
    if islock:
        lock.acquire(True)
    days = data.get_days(user_id)
    start = 1
    end = days
    if islock:
        lock.release()
    return [start, end]


# функция, возвращающая записи в дневнике за последний день
def get_diary_day(user_id, islock=True):
    if islock:
        lock.acquire(True)
    res = []
    i = data.get_days(user_id)
    sql.execute(f"SELECT situation FROM diary WHERE id = {user_id} AND days = {i}")
    situations = sql.fetchall()

    for sit in situations:
        sql.execute(f"SELECT emotion FROM diary WHERE id = {user_id} AND situation = '{sit[0]}'")
        emotion = sql.fetchone()
        emo = (emotion[0], sit[0])
        res.append(emo)
    if islock:
        lock.release()
    return res


# костылечек (не работает)
def what_day(i):
    return ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'][i - 1]


def get_max_key(user_id):
    sql.execute(f"SELECT * FROM diary")
    f = sql.fetchall()
    f.reverse()
    for i in f:
        if i[1] == user_id:
            return i[0]


def day_of_week(user_id, day, islock=True):
    lock.acquire(True)
    number = get_max_key(user_id)
    sql.execute(f'UPDATE diary SET day = "{day}" WHERE key_ = {number}')
    db.commit()
    lock.release()


def get_day_of_week(user_id, islock=True):
    lock.acquire(True)
    number = get_max_key(user_id)
    sql.execute(f'SELECT day_of_week FROM diary WHERE key_ = {number}')


def del_table(islock=True):  # полная очистка базы (WARNING!)
    if islock:
        lock.acquire(True)
    sql.execute(f"DELETE from diary")
    db.commit()
    if islock:
        lock.release()


def analize(user_id, islock=True):
    if islock:
        lock.acquire(True)
    end = data.get_days(user_id)
    res = []
    if end < 11:
        return None
    start = data.get_days(user_id) - 10
    for i in range(start, end + 1):
        sql.execute(f"SELECT situation FROM diary WHERE id = {user_id} AND days = {i}")
        situations = sql.fetchall()
        if len(situations) <= 10:
            return None
        if situations:
            for sit in situations:
                sql.execute(f"SELECT emotion FROM diary WHERE id = {user_id} AND situation = '{sit[0]}'")
                emotion = sql.fetchone()
                res.append(str(emotion[0]) + ' ' + str(sit[0]))
    return res