import sqlite3
from datetime import datetime
from Auth.account import Account
from menu import menu

def create_letter_table():
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS letter (
            letter_id INTEGER PRIMARY KEY,
            account_id INTEGER,
            letter_content VARCHAR,
            sender VARCHAR,
            content TEXT,
            date_received DATE,
            status TEXT CHECK(status IN ('in process', 'completed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(account_id)
        )
    ''')
    conn.commit()
    conn.close()

def add_letter(account_id, letter_content, sender, content, date_received, status):
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO letter (account_id, letter_content, sender, content, date_received, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (account_id, letter_content, sender, content, date_received, status))
    conn.commit()
    conn.close()

def view_letters():
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM letter')
    letters = cursor.fetchall()
    if letters:
        for letter in letters:
            print(f"ID: {letter[0]}, Account: {letter[1]}, Content: {letter[2]}, "
                  f"Sender: {letter[3]}, Text: {letter[4]}, Date: {letter[5]}, "
                  f"Status: {letter[6]}, Created: {letter[7]}, Updated: {letter[8]}")
    else:
        print("No letters found.")
    conn.close()

def edit_letter(letter_id, letter_content, sender, content, date_received, status):
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        UPDATE letter
        SET letter_content = ?, sender = ?, content = ?, 
            date_received = ?, status = ?, update_at = ?
        WHERE letter_id = ?
    ''', (letter_content, sender, content, date_received, status, update_time, letter_id))
    conn.commit()
    conn.close()

def delete_letter(letter_id):
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM letter WHERE letter_id = ?', (letter_id,))
    conn.commit()
    conn.close()

def letter_page(role, account_id):
    while True:
        print("\n=== Letter Management ===")
        print("1. Add Letter")
        print("2. View Letters")
        if role == "admin":
            print("3. Edit Letter")
            print("4. Delete Letter")
        print("5. Back to Main Menu")

        choice = input("Enter choice: ")
        
        if choice == "1":
            letter_content = input("Enter letter content: ")
            sender = input("Enter sender: ")
            content = input("Enter content: ")
            date_received = input("Enter date received (YYYY-MM-DD): ")
            try:
                date_received = datetime.strptime(date_received, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                continue
            status = input("Enter status (in process/completed): ")
            if status not in ['in process', 'completed']:
                print("Invalid status.")
                continue
            add_letter(account_id, letter_content, sender, content, date_received, status)
            
        elif choice == "2":
            view_letters()
            
        elif role == "admin" and choice == "3":
            letter_id = int(input("Enter letter ID: "))
            letter_content = input("Enter new letter content: ")
            sender = input("Enter new sender: ")
            content = input("Enter new content: ")
            date_received = input("Enter new date received (YYYY-MM-DD): ")
            try:
                date_received = datetime.strptime(date_received, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                continue
            status = input("Enter new status (in process/completed): ")
            if status not in ['in process', 'completed']:
                print("Invalid status.")
                continue
            edit_letter(letter_id, letter_content, sender, content, date_received, status)
            
        elif role == "admin" and choice == "4":
            letter_id = int(input("Enter letter ID: "))
            delete_letter(letter_id)
            
        elif choice == "5":
            break
            
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    create_letter_table()
    # Test with admin role
    letter_page("admin", 1)