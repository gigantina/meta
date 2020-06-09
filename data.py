# -*- coding: utf-8 -*-

import threading
import sqlite3

global db, sql, lock
db = sqlite3.connect('data.db', check_same_thread=False)
sql = db.cursor()
lock = threading.Lock()  # для блокировки второго потока, потому что sqlite3 не работает с потоками


def new(user_id, islock=True):  # создание нового пользователя в базе
    if islock:
        lock.acquire(True)
    sql.execute("SELECT id FROM users")
    fetch = sql.fetchone()
    if not fetch:
        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_id, 0, 0, 0, 1))
        db.commit()
    if islock:
        lock.release()

def game(user_id, isGame, islock=True):  # сообщения будут восприниматься как в игре "камень-ножницы-бумага"
    if islock:
        lock.acquire(True)
    sql.execute(f"UPDATE users SET game = {isGame} WHERE id = {user_id}")
    db.commit()
    if islock:
        lock.release()


def get_game(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT game FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    print(res)
    if islock:
        lock.release()
    return res[0]


def situation(user_id, isFeel,
              islock=True):  # сообщение будут записываться как запись ситуации. Обычно после  '/note'
    lock.acquire(True)
    sql.execute(f"UPDATE users SET situation = {isFeel} WHERE id = {user_id}")
    db.commit()
    lock.release()


def get_situation(user_id, islock=True):
    lock.acquire(True)
    sql.execute(f"SELECT situation FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    lock.release()
    return int(res[0])


def get_chats(islock=True):  # возвращает список id всех пользователей
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT id FROM users")
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
    day = get_days(user_id)
    date = get_date(user_id)
    sql.execute("UPDATE diary SET days = days + 1 WHERE id = ?", (user_id,))
    db.commit()
    if islock:
        lock.release()


def utc(user_id, time, islock=True):  # установка часового пояса
    if islock:
        lock.acquire(True)
    sql.execute(f"UPDATE users SET utc = ? WHERE id = ?", (time, user_id))
    db.commit()
    if islock:
        lock.release()


def get_utc(user_id, islock=True):
    if islock:
        lock.acquire(True)
    sql.execute(f"SELECT utc FROM users WHERE id = {user_id}")
    res = sql.fetchone()
    if islock:
        lock.release()
    return res[0]


def del_table(islock=True):  # полная очистка базы (WARNING!)
    if islock:
        lock.acquire(True)
    sql.execute(f"DELETE from users")
    db.commit()
    if islock:
        lock.release()