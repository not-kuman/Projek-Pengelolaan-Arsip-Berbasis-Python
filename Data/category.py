import sqlite3
from datetime import datetime

def buat_tabel():
    """Membuat tabel categories jika belum ada."""
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                   categories_id INTEGER PRIMARY KEY,
                   categories_name VARCHAR(100) UNIQUE,
                   description TEXT,
                   created_at TIMESTAMP,
                   update_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def tambah_categories(categories_name, description):
    """Menambahkan kategori baru ke tabel categories."""
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    created_at = update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        cursor.execute('''INSERT INTO categories (categories_name, description, created_at, update_at)
                          VALUES (?, ?, ?, ?)''', (categories_name, description, created_at, update_at))
        conn.commit()
        print("Category added successfully.")
    except sqlite3.IntegrityError:
        print(f"Category with name '{categories_name}' already exists.")
    finally:
        conn.close()

def lihat_categories():
    """Melihat semua kategori yang ada di tabel categories."""
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM categories')
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No categories found.")

    conn.close()

def edit_categories(categories_id, new_name, new_description):
    """Mengedit kategori berdasarkan ID."""
    if not new_name and not new_description:
        print("No new data provided for update.")
        return

    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''UPDATE categories 
                      SET categories_name = ?, description = ?, update_at = ?
                      WHERE categories_id = ?''', (new_name, new_description, update_at, categories_id))

    if cursor.rowcount > 0:
        print(f"Category with ID {categories_id} updated successfully.")
    else:
        print(f"No category found with ID {categories_id}.")

    conn.commit()
    conn.close()

def hapus_categories(categories_id):
    """Menghapus kategori berdasarkan ID."""
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM categories WHERE categories_id = ?', (categories_id,))

    if cursor.rowcount > 0:
        print(f"Category with ID {categories_id} deleted successfully.")
    else:
        print(f"No category found with ID {categories_id}.")

    conn.commit()
    conn.close()

def halaman_arsip():
    from mainmenu import menu
    print("\n--- Halaman Arsip ---")
    print("1. Tambah data arsip")
    print("2. Lihat data arsip")
    print("3. Edit data arsip")
    print("4. Hapus data arsip")
    print("5. Tampilkan data arsip")
    print("6. Kembali ke Menu Utama")

    try:
        pilihan = int(input("Masukkan pilihan: "))
        if pilihan == 1:
            categories_name = input("Masukkan nama kategori: ")
            description = input("Masukkan deskripsi kategori: ")
            tambah_categories(categories_name, description)
        elif pilihan == 2:
            lihat_categories()
        elif pilihan == 3:
            categories_id = int(input("Masukkan ID kategori: "))
            new_name = input("Masukkan nama baru kategori: ")
            new_description = input("Masukkan deskripsi baru kategori: ")
            edit_categories(categories_id, new_name, new_description)
        elif pilihan == 4:
            categories_id = int(input("Masukkan ID kategori: "))
            hapus_categories(categories_id)
        elif pilihan == 5:
            lihat_categories()
        elif pilihan == 6:
            print("Anda Akan Kembali Ke Menu Utama!!")
            menu()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
            halaman_arsip()
    except ValueError:
        print("Masukkan angka untuk memilih. Silakan coba lagi.")
        halaman_arsip()

if __name__ == "__main__":
    halaman_arsip()
