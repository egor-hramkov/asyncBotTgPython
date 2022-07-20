import sqlite3

def create_table():
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS waiting_rooms(
        waiting INT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS chat_rooms(
        first_user INT,
        second_user INT
    )""")
    db.commit()
    db.close()

def add_waiting(user_id):
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    cur.execute(f"INSERT INTO waiting_rooms VALUES (?)", (user_id,))
    db.commit()
    db.close()

def add_chating(id_first_user, id_second_user):
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    cur.execute(f"INSERT INTO chat_rooms VALUES (?, ?)", (id_first_user, id_second_user))
    db.commit()
    db.close()

def take_waiting(user_id):
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    cur.execute(f"SELECT waiting FROM waiting_rooms WHERE waiting = ?", (user_id,))
    ret = cur.fetchone()
    db.close()
    return ret

def pop_waiting():
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    try:
        cur.execute(f"SELECT waiting FROM waiting_rooms LIMIT 1")
        ret = cur.fetchone()
        cur.execute(f"DELETE FROM waiting_rooms WHERE (SELECT * FROM waiting_rooms LIMIT 1)")
        db.commit()
        db.close()
        return ret
    except sqlite3.Error:
        db.close()
        return None

def check_waiting():
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM waiting_rooms")
    ret = cur.fetchone()
    db.close()
    return ret

def delete_waiting(user_id):
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    try:
        cur.execute(f"DELETE FROM waiting_rooms WHERE waiting = ?", (user_id,))
        ret = cur.fetchone()
        db.commit()
        db.close()
        return ret
    except sqlite3.Error:
        db.close()
        return None

def take_chat(user_id):
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    cur.execute(f"SELECT second_user FROM chat_rooms WHERE first_user = ?", (user_id,))
    ret = cur.fetchone()
    db.close()
    return ret

def delete_chat_rooms(user_id):
    db = sqlite3.connect('server.db')
    cur = db.cursor()
    try:
        cur.execute(f"DELETE FROM chat_rooms WHERE first_user = ?", (user_id,))
        ret = cur.fetchone()
        db.commit()
        db.close()
        return ret
    except sqlite3.Error:
        db.close()
        return None