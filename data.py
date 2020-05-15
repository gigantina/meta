# -*- coding: utf-8 -*-

import sqlite3

global db
global sql
db = sqlite3.connect('data.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT,
        game INT
        )""")
db.commit()


def new(user_id):
    global sql, db
    sql.execute("SELECT id FROM users")
    if sql.fetchone() == None:
        sql.execute(f"INSERT INTO users VALUES (?, ?)", (user_id, 0))
        db.commit()


def game(user_id, isGame):
    global sql, db
    sql.execute(f"UPDATE users SET game = {isGame} WHERE id = {user_id}")
    db.commit()


def get_game(user_id):
    sql.execute(f"SELECT game FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    return res
