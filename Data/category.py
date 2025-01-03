import sqlite3
from datetime import datetime

def create_db_connection():
    return sqlite3.connect('DB_Arsip.db')

def init_db():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
        categories_id INTEGER PRIMARY KEY AUTOINCREMENT,
        categories_name VARCHAR(100) UNIQUE,
        categories_code VARCHAR(50) UNIQUE,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def tambah_kategori():
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        name = input("Masukkan nama kategori: ").strip()
        code = input("Masukkan kode kategori: ").strip()
        desc = input("Masukkan deskripsi: ").strip()
        
        if not all([name, code, desc]):
            print("Semua field harus diisi!")
            return
            
        cursor.execute("""
            INSERT INTO categories (categories_name, categories_code, description)
            VALUES (?, ?, ?)""", (name, code, desc))
        conn.commit()
        print("Kategori berhasil ditambahkan.")
    except sqlite3.IntegrityError as e:
        if "categories_name" in str(e):
            print("Nama kategori sudah digunakan.")
        elif "categories_code" in str(e):
            print("Kode kategori sudah digunakan.")
    finally:
        conn.close()

def lihat_kategori():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    
    if categories:
        print("\nDaftar Kategori:")
        for cat in categories:
            print(f"""
ID: {cat[0]}
Nama: {cat[1]}
Kode: {cat[2]}
Deskripsi: {cat[3]}
Dibuat: {cat[4]}
Diperbarui: {cat[5]}
------------------------""")
    else:
        print("Tidak ada kategori.")
    conn.close()

def edit_kategori():
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        lihat_kategori()
        cat_id = int(input("\nMasukkan ID kategori yang ingin diedit: "))
        
        cursor.execute("SELECT * FROM categories WHERE categories_id = ?", (cat_id,))
        if not cursor.fetchone():
            print("Kategori tidak ditemukan.")
            return
            
        name = input("Nama baru (Enter untuk tidak mengubah): ").strip()
        code = input("Kode baru (Enter untuk tidak mengubah): ").strip()
        desc = input("Deskripsi baru (Enter untuk tidak mengubah): ").strip()
        
        updates = []
        values = []
        if name:
            updates.append("categories_name = ?")
            values.append(name)
        if code:
            updates.append("categories_code = ?")
            values.append(code)
        if desc:
            updates.append("description = ?")
            values.append(desc)
            
        if updates:
            updates.append("update_at = CURRENT_TIMESTAMP")
            query = f"UPDATE categories SET {', '.join(updates)} WHERE categories_id = ?"
            values.append(cat_id)
            cursor.execute(query, values)
            conn.commit()
            print("Kategori berhasil diperbarui.")
        else:
            print("Tidak ada perubahan dilakukan.")
            
    except ValueError:
        print("ID harus berupa angka.")
    except sqlite3.IntegrityError as e:
        if "categories_name" in str(e):
            print("Nama kategori sudah digunakan.")
        elif "categories_code" in str(e):
            print("Kode kategori sudah digunakan.")
    finally:
        conn.close()

def hapus_kategori():
    conn = create_db_connection()
    cursor = conn.cursor()
    try:
        lihat_kategori()
        cat_id = int(input("\nMasukkan ID kategori yang ingin dihapus: "))
        
        cursor.execute("SELECT * FROM categories WHERE categories_id = ?", (cat_id,))
        if not cursor.fetchone():
            print("Kategori tidak ditemukan.")
            return
            
        confirm = input("Konfirmasi hapus? (y/n): ").lower()
        if confirm == 'y':
            cursor.execute("DELETE FROM categories WHERE categories_id = ?", (cat_id,))
            conn.commit()
            print("Kategori berhasil dihapus.")
    except ValueError:
        print("ID harus berupa angka.")
    finally:
        conn.close()

def halaman_kategori(role):
    init_db()
    while True:
        print("\n--- Halaman Kategori ---")
        if role == "admin":
            print("1. Tambah Kategori")
            print("2. Lihat Kategori")
            print("3. Edit Kategori")
            print("4. Hapus Kategori")
            print("5. Kembali")
            
            try:
                pilihan = int(input("Pilihan: "))
                if pilihan == 1:
                    tambah_kategori()
                elif pilihan == 2:
                    lihat_kategori()
                elif pilihan == 3:
                    edit_kategori()
                elif pilihan == 4:
                    hapus_kategori()
                elif pilihan == 5:
                    break
                else:
                    print("Pilihan tidak valid.")
            except ValueError:
                print("Masukkan angka.")
        else:
            print("1. Tambah Kategori")
            print("2. Lihat Kategori") 
            print("3. Kembali")
            
            try:
                pilihan = int(input("Pilihan: "))
                if pilihan == 1:
                    tambah_kategori()
                elif pilihan == 2:
                    lihat_kategori()
                elif pilihan == 3:
                    break
                else:
                    print("Pilihan tidak valid.")
            except ValueError:
                print("Masukkan angka.")