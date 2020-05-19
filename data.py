# -*- coding: utf-8 -*-

import threading
import sqlite3

global db, sql, lock
db = sqlite3.connect('data.db', check_same_thread=False)
sql = db.cursor()
lock = threading.Lock()


def create():
    lock.acquire(True)

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
            id INT,
            game INT,
            feel INT,
            situation INT,
            days INT
            )""")
    db.commit()
    lock.release()


def new(user_id, islock=True):
    lock.acquire(True)
    sql.execute("SELECT id FROM users")
    if not sql.fetchone():
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_id, 0, 0, 0, 1))
        db.commit()
    lock.release()


def game(user_id, isGame, islock=True):
    lock.acquire(True)
    sql.execute(f"UPDATE users SET game = {isGame} WHERE id = {user_id}")
    db.commit()
    lock.release()


def get_game(user_id, islock=True):
    lock.acquire(True)
    sql.execute(f"SELECT game FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    lock.release()
    return res[0]


def feel(user_id, isFeel, islock=True):
    lock.acquire(True)
    sql.execute(f"UPDATE users SET feel = {isFeel} WHERE id = {user_id}")
    db.commit()
    lock.release()


def get_feel(user_id, islock=True):
    lock.acquire(True)
    sql.execute(f"SELECT feel FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    lock.release()
    return res[0]


def situation(user_id, isFeel, islock=True):
    lock.acquire(True)
    sql.execute(f"UPDATE users SET situation = {isFeel} WHERE id = {user_id}")
    db.commit()
    lock.release()


def get_situation(user_id, islock=True):
    lock.acquire(True)
    sql.execute(f"SELECT situation FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    lock.release()
    return res[0]


def get_chats(islock=True):
    lock.acquire(True)
    sql.execute(f"SELECT chat FROM users")
    res = [i for i in sql.fetchall()]
    lock.release()
    return res


def get_days(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT days FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    if islock:
        lock.release()
    return res[0]


def new_day(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"UPDATE diary SET days = days + 1 WHERE id = {user_id}")
    db.commit()
    if islock:
        lock.release()
