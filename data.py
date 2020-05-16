# -*- coding: utf-8 -*-

import threading
import sqlite3

global db
global sql
db = sqlite3.connect('data.db', check_same_thread=False)
sql = db.cursor()


lock = threading.Lock()
lock.acquire(True)

sql.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT,
        chat INT,
        game INT
        )""")
db.commit()
lock.release()

def new(user_id, chat_id):
    lock = threading.Lock()
    lock.acquire(True)
    sql.execute("SELECT id FROM users")
    if sql.fetchone() == None:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_id, chat_id, 0))
        db.commit()
    lock.release()


def game(user_id, isGame):
    lock = threading.Lock()
    lock.acquire(True)
    sql.execute(f"UPDATE users SET game = {isGame} WHERE id = {user_id}")
    db.commit()
    lock.release()


def get_game(user_id):
    lock = threading.Lock()
    lock.acquire(True)
    sql.execute(f"SELECT game FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    print(res)
    lock.release()
    return res[0]

def get_chats():
    lock = threading.Lock()
    lock.acquire(True)
    sql.execute(f"SELECT chat FROM users")
    res = [i for i in sql.fetchall()]
    lock.release()
    return res
