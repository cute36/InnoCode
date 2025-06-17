import sqlite3
def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (user_id INTEGER PRIMARY KEY,
                      username TEXT,
                      first_name TEXT)''')
    conn.commit()
    conn.close()


def add_user(user_id, username=None, first_name=None):
    """Добавляет или обновляет пользователя в базе данных"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name
        ''', (user_id, username, first_name))

        conn.commit()
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
    finally:
        conn.close()


def show_all_users():
    """Показывает всех пользователей из базы данных"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    print("\nСписок пользователей:")
    print("ID       | Username       | First Name")
    print("-" * 40)
    for user in users:
        print(f"{user[0]:<8} | {user[1] or 'None':<14} | {user[2] or 'None'}")

    conn.close()


def get_user_by_username(username: str):
    """Ищет пользователя по юзернейму в базе данных"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    conn.close()
    return user


def save_user_to_db(user_id: int, username: str, first_name: str, is_bot: bool = False):
    """Сохраняет пользователя в базу данных"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
        ''', (user_id, username, first_name))

        conn.commit()
    except Exception as e:
        print(f"Ошибка при сохранении пользователя: {e}")
    finally:
        conn.close()
# Инициализация при импорте
init_db()
show_all_users()