from contextlib import contextmanager

import mysql.connector

from app.core.config import DB_CONFIG


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@contextmanager
def db_cursor(dictionary=True):
    db = get_db()
    cur = db.cursor(dictionary=dictionary)
    try:
        yield db, cur
    finally:
        cur.close()
        db.close()
