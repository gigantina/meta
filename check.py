import threading
import sqlite3
import functions as f

global db, sql, lock
db = sqlite3.connect('check.db', check_same_thread=False)
sql = db.cursor()
lock = threading.Lock()


def new(user_id, islock=True):  # создание нового пользователя в базе
    if islock:
        lock.acquire(True)
    sql.execute("SELECT id FROM check_days")
    fetch = sql.fetchone()
    if not fetch:
        sql.execute(f"INSERT INTO check_days VALUES (?, ?, ?)", (user_id, 0, 0))
        db.commit()
    if islock:
        lock.release()

def tuesday_set(user_id, value, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"UPDATE check_days SET first_ = {value} WHERE id = {user_id}")
    db.commit()
    if islock:
        lock.release()


def get_tuesday(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT first_ FROM check_days WHERE id = {user_id}")
    res = sql.fetchone()
    if islock:
        lock.release()
    return res[0]


def friday_set(user_id, value, islock=True):
    if islock:
        lock.acquire(True)

    sql.execute(f"UPDATE check_days SET second_ = {value} WHERE id = {user_id}")
    db.commit()
    if islock:
        lock.release()


def get_friday(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT second_ FROM check_days WHERE id = {user_id}")
    res = sql.fetchone()
    if islock:
        lock.release()
    return res[0]

def get_date(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT date_reg FROM check_days WHERE id = {user_id}")
    res = sql.fetchone()
    if islock:
        lock.release()
    return res[0]

def del_table():
    sql.execute("DELETE FROM check_days")
    db.commit()