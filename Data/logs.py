import sqlite3
import datetime


DATABASE_NAME = 'DB_Arsip.db'
def create_db_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)

def create_users_table():
    """Create the account table if it doesn't exist."""
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS account (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
        )
    ''')
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
    """
    Log an action performed by a user into the database.
    Args:
        action (str): The action performed (e.g., 'Create', 'View', 'Update', 'Delete').
        username (str): The username of the account performing the action.
    """
    valid_actions = {'Create', 'View', 'Update', 'Delete'}
    if action not in valid_actions:
        raise ValueError(f"Invalid action. Must be one of {valid_actions}")
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT account_id FROM account WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        account_id = result[0]
        cursor.execute('''
            INSERT INTO logs (account_id, action)
            VALUES (?, ?)
        ''', (account_id, action))
        conn.commit()
        print(f"Action '{action}' logged for user '{username}'.")
    else:
        print(f"User '{username}' not found. Action '{action}' not logged.")
    conn.close()

def get_account_activity():
    """
    Retrieve and display all account activity logs from the database.
    """
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT logs.logs_id, account.username, logs.action, logs.timestamp
        FROM logs
        JOIN account ON logs.account_id = account.account_id
        ORDER BY logs.timestamp DESC
    ''')
    logs = cursor.fetchall()
    if logs:
        print("\n=== Account Activity Logs ===")
        for log in logs:
            log_id, username, action, timestamp = log
            print(f"[{timestamp}] User: {username}, Action: {action} (Log ID: {log_id})")
    else:
        print("\nNo activity logs available.")
    conn.close()

def add_log_to_file(message):
    """
    Write a log message to a text file with a timestamp.
    Args:
        message (str): The log message to be written.
    """
    with open("logs.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

def view_logs_from_file():
    """
    Display all logs stored in the log file.
    """
    try:
        with open("logs.txt", "r") as log_file:
            logs = log_file.readlines()
            if logs:
                print("\n=== Logs from File ===")
                for log in logs:
                    print(log.strip())
            else:
                print("\nNo logs available in the file.")
    except FileNotFoundError:
        print("\nLog file not found.")
