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

def log_action(action, username):
    valid_actions = {'Create', 'View', 'Update', 'Delete'}
    if action not in valid_actions:
        raise ValueError(f"Invalid action. Must be one of {valid_actions}")
    # Implement the logging logic here
    print(f"Action: {action}, User: {username}")

def get_account_activity():
    # Implement the logic to get account activity here
    print("Menampilkan aktivitas akun...")
