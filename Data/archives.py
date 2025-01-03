import sqlite3
from datetime import datetime

def create_db_connection():
    return sqlite3.connect('DB_Arsip.db')

def init_db():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS archives (
        archives_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        account_id INTEGER,
        title TEXT,
        description TEXT,
        file_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES category(category_id),
        FOREIGN KEY (account_id) REFERENCES account(account_id)
    )''')
    conn.commit()
    conn.close()

def tambah_arsip(account_id):
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        title = input("Masukkan Title: ")
        description = input("Masukkan Description: ")
        file_path = input("Masukkan File Path: ")
        category_id = int(input("Masukkan Category ID: "))
        
        cursor.execute("SELECT category_id FROM category WHERE category_id = ?", (category_id,))
        if not cursor.fetchone():
            print("Category ID tidak ditemukan.")
            return
            
        cursor.execute("""
            INSERT INTO archives (category_id, account_id, title, description, file_path)
            VALUES (?, ?, ?, ?, ?)""", 
            (category_id, account_id, title, description, file_path))
        conn.commit()
        print("Data arsip berhasil ditambahkan!")
    except ValueError:
        print("Input tidak valid. Pastikan Category ID berupa angka.")
    except sqlite3.Error as e:
        print(f"Kesalahan database: {e}")
    finally:
        conn.close()

def lihat_arsip(account_id, is_admin=False):
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        if is_admin:
            cursor.execute("""
                SELECT a.*, c.name as category_name, ac.username 
                FROM archives a 
                LEFT JOIN category c ON a.category_id = c.category_id
                LEFT JOIN account ac ON a.account_id = ac.account_id
            """)
        else:
            cursor.execute("""
                SELECT a.*, c.name as category_name, ac.username 
                FROM archives a 
                LEFT JOIN category c ON a.category_id = c.category_id
                LEFT JOIN account ac ON a.account_id = ac.account_id
                WHERE a.account_id = ?
            """, (account_id,))
        
        rows = cursor.fetchall()
        if rows:
            print("\nData Arsip:")
            for row in rows:
                print(f"""
ID: {row[0]}
Category: {row[8]}
Created by: {row[9]}
Title: {row[3]}
Description: {row[4]}
File Path: {row[5]}
Created: {row[6]}
Updated: {row[7]}
------------------------""")
        else:
            print("Tidak ada data arsip.")
    except sqlite3.Error as e:
        print(f"Kesalahan database: {e}")
    finally:
        conn.close()

def edit_arsip(account_id, is_admin=False):
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        archives_id = int(input("Masukkan ID arsip yang ingin diubah: "))
        
        if is_admin:
            cursor.execute("SELECT * FROM archives WHERE archives_id = ?", (archives_id,))
        else:
            cursor.execute("""
                SELECT * FROM archives 
                WHERE archives_id = ? AND account_id = ?
            """, (archives_id, account_id))
            
        archive = cursor.fetchone()
        if not archive:
            print("Arsip tidak ditemukan atau Anda tidak memiliki akses.")
            return
            
        title = input("Masukkan Title Baru (Enter untuk tidak mengubah): ") or archive[3]
        description = input("Masukkan Description Baru (Enter untuk tidak mengubah): ") or archive[4]
        file_path = input("Masukkan File Path Baru (Enter untuk tidak mengubah): ") or archive[5]
        category_id = input("Masukkan Category ID Baru (Enter untuk tidak mengubah): ")
        
        if category_id:
            category_id = int(category_id)
            cursor.execute("SELECT category_id FROM category WHERE category_id = ?", (category_id,))
            if not cursor.fetchone():
                print("Category ID tidak ditemukan.")
                return
        else:
            category_id = archive[1]

        cursor.execute("""
            UPDATE archives 
            SET title = ?, description = ?, file_path = ?, category_id = ?, 
                updated_at = CURRENT_TIMESTAMP 
            WHERE archives_id = ?""", 
            (title, description, file_path, category_id, archives_id))
        conn.commit()
        print("Data arsip berhasil diperbarui!")
    except ValueError:
        print("Input tidak valid. Pastikan ID berupa angka.")
    except sqlite3.Error as e:
        print(f"Kesalahan database: {e}")
    finally:
        conn.close()

def hapus_arsip(account_id, is_admin=False):
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        archives_id = int(input("Masukkan ID arsip yang ingin dihapus: "))
        
        if is_admin:
            cursor.execute("SELECT * FROM archives WHERE archives_id = ?", (archives_id,))
        else:
            cursor.execute("""
                SELECT * FROM archives 
                WHERE archives_id = ? AND account_id = ?
            """, (archives_id, account_id))
            
        if not cursor.fetchone():
            print("Arsip tidak ditemukan atau Anda tidak memiliki akses.")
            return

        if input("Konfirmasi penghapusan (y/n): ").lower() == 'y':
            cursor.execute("DELETE FROM archives WHERE archives_id = ?", (archives_id,))
            conn.commit()
            print("Data arsip berhasil dihapus!")
        else:
            print("Penghapusan dibatalkan.")
    except ValueError:
        print("Input tidak valid. Pastikan ID berupa angka.")
    except sqlite3.Error as e:
        print(f"Kesalahan database: {e}")
    finally:
        conn.close()
def halaman_arsip(account_id, role):
    init_db()
    
    if role == "admin":
        while True:
            print("\n--- Halaman Arsip Admin ---")
            print("1. Tambah data arsip")
            print("2. Lihat semua data arsip")
            print("3. Edit data arsip")
            print("4. Hapus data arsip")
            print("5. Kembali ke Menu Admin")
            
            try:
                pilihan = int(input("Masukkan pilihan: "))
                if pilihan == 1:
                    tambah_arsip(account_id)
                elif pilihan == 2:
                    lihat_arsip(account_id, True)
                elif pilihan == 3:
                    edit_arsip(account_id, True)
                elif pilihan == 4:
                    hapus_arsip(account_id, True)
                elif pilihan == 5:
                    break
                else:
                    print("Pilihan tidak valid.")
            except ValueError:
                print("Masukkan angka untuk memilih.")
    else:
        while True:
            print("\n--- Halaman Arsip User ---")
            print("1. Tambah data arsip")
            print("2. Lihat data arsip")
            print("3. Kembali ke Menu User")
            
            try:
                pilihan = int(input("Masukkan pilihan: "))
                if pilihan == 1:
                    tambah_arsip(account_id)
                elif pilihan == 2:
                    lihat_arsip(account_id, False)
                elif pilihan == 3:
                    break
                else:
                    print("Pilihan tidak valid.")
            except ValueError:
                print("Masukkan angka untuk memilih.")