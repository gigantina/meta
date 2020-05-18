import threading
import sqlite3

global db, sql, lock
db = sqlite3.connect('data-emotions-amount.db', check_same_thread=False)
sql = db.cursor()
lock = threading.Lock()


def create():
    lock.acquire(True)

    sql.execute("""CREATE TABLE IF NOT EXISTS diary (
            id INT,
            situation TEXT,
            emotion TEXT,
            days INT
            )""")
    db.commit()
    lock.release()


def what_emotion(emotion, islock=True):
    res = None
    if emotion == 'грусть':
        res = "sad"
    elif emotion == 'гнев':
        res = "anger"
    elif emotion == 'радость':
        res = "joy"
    elif emotion == 'вина':
        res = "fault"
    elif emotion == 'тревога':
        res = "fear"
    return res



def new_week(user_id, islock=True):
    lock.acquire(True)
    for emotion in ['sad', 'joy', 'anger', 'fault', 'fear']:
        sql.execute(f"UPDATE diary SET {emotion} + '_week' = 0 WHERE id = {user_id}")
        db.commit()
    lock.release()
