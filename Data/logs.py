import sqlite3
import re
import datetime

def create_db_connection():
    return sqlite3.connect('DB_Arsip.db')

def create_users_table():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS account (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
    )''')
    conn.commit()
    conn.close()


def create_logs_table():
    """Create the logs table if it doesn't exist."""
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            logs_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            archives_id INTEGER,
            letter_id INTEGER,
            action TEXT CHECK(action IN ('Create', 'Update', 'Delete', 'View')),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES account(account_id)
        )
    ''')
    conn.commit()
    conn.close()

def log_action(account_id, action, archives_id=None, letter_id=None):
    """
    Log an action to the database.
    """
    valid_actions = {'Create', 'Update', 'Delete', 'View'}
    if action not in valid_actions:
        raise ValueError(f"Invalid action. Must be one of {valid_actions}")

    try:
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO logs (account_id, action, archives_id, letter_id)
            VALUES (?, ?, ?, ?)
        ''', (account_id, action, archives_id, letter_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def get_account_activity(account_id):
    """
    Retrieve activity logs for a specific account.
    """
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT logs_id, action, archives_id, letter_id, timestamp
        FROM logs
        WHERE account_id = ?
        ORDER BY timestamp DESC
    ''', (account_id,))
    activities = cursor.fetchall()
    conn.close()
    
    if activities:
        for log in activities:
            print(f"Log ID: {log[0]}, Action: {log[1]}, Archives ID: {log[2]}, "
                  f"Letter ID: {log[3]}, Time: {log[4]}")
    else:
        print(f"No activity found for Account ID {account_id}")
