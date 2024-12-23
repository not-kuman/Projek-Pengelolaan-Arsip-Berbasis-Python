import sqlite3
from datetime import datetime

def create_db_connection():
    """Helper function to create and return a database connection."""
    return sqlite3.connect('DB_Arsip.db')

def buat_tabel_kategori():
    """Membuat tabel categories jika belum ada."""
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                   categories_id INTEGER PRIMARY KEY,
                   categories_name VARCHAR(100) UNIQUE,
                   description TEXT,
                   created_at TIMESTAMP,
                   update_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def tambah_kategori(categories_name, description):
    """Menambahkan kategori baru ke tabel categories."""
    conn = create_db_connection()
    cursor = conn.cursor()
    created_at = update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        cursor.execute('''INSERT INTO categories (categories_name, description, created_at, update_at)
                          VALUES (?, ?, ?, ?)''', (categories_name, description, created_at, update_at))
        conn.commit()
        print("Kategori berhasil ditambahkan.")
    except sqlite3.IntegrityError:
        print(f"Kategori dengan nama '{categories_name}' sudah ada.")
    finally:
        conn.close()

def lihat_kategori():
    """Melihat semua kategori yang ada di tabel categories."""
    conn = create_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM categories')
    rows = cursor.fetchall()

    if rows:
        print("\nDaftar Kategori:")
        for row in rows:
            print(f"ID: {row[0]}, Nama: {row[1]}, Deskripsi: {row[2]}, Dibuat: {row[3]}, Diperbarui: {row[4]}")
    else:
        print("Tidak ada kategori yang ditemukan.")

    conn.close()

def edit_kategori(categories_id, new_name, new_description):
    """Mengedit kategori berdasarkan ID."""
    conn = create_db_connection()
    cursor = conn.cursor()
    update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        cursor.execute('''UPDATE categories 
                          SET categories_name = ?, description = ?, update_at = ?
                          WHERE categories_id = ?''', (new_name, new_description, update_at, categories_id))

        if cursor.rowcount > 0:
            print(f"Kategori dengan ID {categories_id} berhasil diperbarui.")
        else:
            print(f"Kategori dengan ID {categories_id} tidak ditemukan.")
    except sqlite3.IntegrityError:
        print("Nama kategori sudah digunakan.")
    finally:
        conn.commit()
        conn.close()

def hapus_kategori(categories_id):
    """Menghapus kategori berdasarkan ID."""
    conn = create_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM categories WHERE categories_id = ?', (categories_id,))

    if cursor.rowcount > 0:
        print(f"Kategori dengan ID {categories_id} berhasil dihapus.")
    else:
        print(f"Kategori dengan ID {categories_id} tidak ditemukan.")

    conn.commit()
    conn.close()

def halaman_kategori(role):
    """Halaman utama untuk mengelola kategori."""
    buat_tabel_kategori()
    while True:
        print("\n--- Halaman Kategori ---")
        print("1. Tambah Kategori")
        print("2. Lihat Kategori")
        if role == "admin":
            print("3. Edit Kategori")
            print("4. Hapus Kategori")
        print("5. Kembali ke Menu Utama")

        try:
            pilihan = int(input("Masukkan pilihan: "))
            if pilihan == 1:
                categories_name = input("Masukkan nama kategori: ").strip()
                description = input("Masukkan deskripsi kategori: ").strip()
                if not categories_name or not description:
                    print("Nama dan deskripsi kategori tidak boleh kosong!")
                else:
                    tambah_kategori(categories_name, description)
            elif pilihan == 2:
                lihat_kategori()
            elif pilihan == 3 and role == "admin":
                try:
                    categories_id = int(input("Masukkan ID kategori yang ingin diedit: "))
                    new_name = input("Masukkan nama baru kategori: ").strip()
                    new_description = input("Masukkan deskripsi baru kategori: ").strip()
                    if not new_name or not new_description:
                        print("Nama dan deskripsi baru tidak boleh kosong!")
                    else:
                        edit_kategori(categories_id, new_name, new_description)
                except ValueError:
                    print("ID kategori harus berupa angka.")
            elif pilihan == 4 and role == "admin":
                try:
                    categories_id = int(input("Masukkan ID kategori yang ingin dihapus: "))
                    hapus_kategori(categories_id)
                except ValueError:
                    print("ID kategori harus berupa angka.")
            elif pilihan == 5:
                print("Kembali ke Menu Utama.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Masukkan angka untuk memilih opsi.")

if __name__ == "__main__":
    # Tentukan role pengguna ('admin' atau 'user')
    role = "admin"  # Ubah sesuai kebutuhan
    halaman_kategori(role)
