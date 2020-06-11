import sqlite3

from definitions import DATABASE_PATH

connection = None   # Active database connection


def get_connection():
    global connection
    if not connection:
        connection = sqlite3.connect(DATABASE_PATH)
    return connection


def close_connection():
    connection.close()


def create_twitchuser_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE TwitchUsers (user_id INTEGER PRIMARY KEY, user_name text)''')
    conn.commit()
    cursor.close()

    # Username -> UserID


def add_twitchuser_row(user_id: str, username: str):
    conn = get_connection()
    conn.execute(f"INSERT INTO TwitchUsers (user_id, user_name) VALUES ('{user_id}', '{username}')")
    conn.commit()


def get_twitchuser_rows():
    conn = get_connection()
    return conn.execute(f'SELECT * FROM TwitchUsers').fetchall()


def remove_twitchuser(username):
    conn = get_connection()
    conn.execute(f"DELETE FROM TwitchUsers WHERE user_name='{username}'")
    conn.commit()


def clear_twitchrows():
    conn = get_connection()
    conn.execute(f"DELETE FROM TwitchUsers")
    conn.commit()


if __name__ == '__main__':
    clear_twitchrows()
