import datetime
import os
import sqlite3


def log_action(action, username):
    """
    Log an action performed by a user to a log file.

    Args:
        action (str): The action performed.
        username (str): The username of the performer.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] Action: {action}, Performed by: {username}\n"
    rotate_logs()
    with open("logs.txt", "a") as log_file:
        log_file.write(log_message)

def rotate_logs():
    """
    Rotate the log file if it exceeds the maximum size.
    """
    log_file = "logs.txt"
    max_size = 5 * 1024 * 1024  # 5 MB
    if os.path.exists(log_file) and os.path.getsize(log_file) > max_size:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.rename(log_file, f"logs_{timestamp}.txt")
        print(f"Log file rotated. Old log saved as logs_{timestamp}.txt.")

def buat_tabel():
    """
    Create the logs table in the SQLite database if it doesn't already exist.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                logs_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT CHECK(action IN ('Create', 'Update', 'Delete')),
                archives_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (archives_id) REFERENCES archives(archives_id)
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        log_action(f"Database Error: {e}", "system")
        print(f"Error creating table: {e}")
    finally:
        conn.close()

def log_to_db(user_id, action, archives_id=None):
    """
    Log an action to the SQLite database.

    Args:
        user_id (int): The ID of the user performing the action.
        action (str): The action performed ('Create', 'Update', 'Delete').
        archives_id (int, optional): The ID of the archive affected by the action. Default is None.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (user_id, action, archives_id)
            VALUES (?, ?, ?)
        ''', (user_id, action, archives_id))
        conn.commit()
    except sqlite3.Error as e:
        log_action(f"Database Error: {e}", "system")
        print(f"Error logging to database: {e}")
    finally:
        conn.close()

def lihat_aktivitas_user(user_id):
    """
    Retrieve and display the activity logs of a specific user.

    Args:
        user_id (int): The ID of the user whose logs are to be retrieved.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT logs_id, action, archives_id, timestamp
            FROM logs
            WHERE user_id = ?''', (user_id,))
        aktivitas = cursor.fetchall()
        if aktivitas:
            for log in aktivitas:
                print(f"Log_ID: {log[0]}, Action: {log[1]}, Archive ID: {log[2]}, Timestamp: {log[3]}")
        else:
            print(f"Belum Ada Aktivitas User ID: {user_id}")
    except sqlite3.Error as e:
        log_action(f"Database Error: {e}", "system")
        print(f"Error retrieving user activity: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    buat_tabel()
    user_id = 1
    log_to_db(user_id, "Create", archives_id=123)
    lihat_aktivitas_user(user_id)
