import sqlite3
from datetime import datetime
from Auth.account import Account

DATABASE_NAME = 'DB_Arsip.db'
account = Account()
role = account.login()


def create_db_connection():
    """Helper function to create and return a database connection."""
    return sqlite3.connect(DATABASE_NAME)

def get_user_role(username):
    """Mendapatkan role user dari tabel account."""
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM account WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print("User tidak ditemukan")
        return None

def buat_tabel_kategori():
    """Membuat tabel categories jika belum ada."""
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                   categories_id INTEGER PRIMARY KEY,
                   categories_name VARCHAR(100) UNIQUE,
                   categories_code VARCHAR(100) UNIQUE,
                   description TEXT,
                   created_at TIMESTAMP,
                   update_at TIMESTAMP)''')
    conn.commit()
    conn.close()

def tambah_kategori(categories_name, categories_code, description):
    """Menambahkan kategori baru ke tabel categories."""
    conn = create_db_connection()
    cursor = conn.cursor()
    created_at = update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute('''INSERT INTO categories (categories_name, categories_code, description, created_at, update_at)
                          VALUES (?, ?, ?, ?, ?)''', 
                          (categories_name, categories_code, description, created_at, update_at))
        conn.commit()
        print("Kategori berhasil ditambahkan.")
    except sqlite3.IntegrityError:
        print(f"Kategori dengan nama '{categories_name}' atau kode '{categories_code}' sudah ada.")
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
            print(f"ID: {row[0]}, Nama: {row[1]}, Kode: {row[2]}, Deskripsi: {row[3]}, Dibuat: {row[4]}, Diperbarui: {row[5]}")
    else:
        print("Tidak ada kategori yang ditemukan.")

    conn.close()

def edit_kategori(categories_id, new_name, new_code, new_description):
    """Mengedit kategori berdasarkan ID."""
    conn = create_db_connection()
    cursor = conn.cursor()
    update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute('''UPDATE categories 
                          SET categories_name = ?, categories_code = ?, description = ?, update_at = ?
                          WHERE categories_id = ?''', 
                          (new_name, new_code, new_description, update_at, categories_id))
        if cursor.rowcount > 0:
            print(f"Kategori dengan ID {categories_id} berhasil diperbarui.")
        else:
            print(f"Kategori dengan ID {categories_id} tidak ditemukan.")
    except sqlite3.IntegrityError:
        print("Nama atau kode kategori sudah digunakan.")
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

def halaman_kategori():
    """Menampilkan halaman kategori dengan mengecek role dari tabel account."""
    buat_tabel_kategori()
    from Auth.account import Account
    from mainmenu import menu
    global role
    if role is None:
        print("Silakan login terlebih dahulu")
        return
    while True:
        print("\n--- Halaman Kategori ---")
        print("1. Tambah Kategori")
        print("2. Lihat Kategori")
        print("3. Edit Kategori")
        print("4. Hapus Kategori")
        print("5. Kembali ke Menu user/admin")
        print("6. Kembali ke Menu Login")
        print("7. Kembali ke Menu Utama")
        try:
            pilihan = int(input("Masukkan pilihan: "))
            if pilihan == 1:
                    categories_name = input("Masukkan nama kategori: ").strip()
                    categories_code = input("Masukkan kode kategori: ").strip()
                    description = input("Masukkan deskripsi kategori: ").strip()
                    if not categories_name or not categories_code or not description:
                        print("Nama, kode, dan deskripsi kategori tidak boleh kosong!")
                    else:
                        tambah_kategori(categories_name, categories_code, description)
            elif pilihan == 2:
                lihat_kategori()
            elif pilihan == 3:
                if role == 'admin':
                    try:
                        categories_id = int(input("Masukkan ID kategori yang ingin diedit: "))
                        new_name = input("Masukkan nama baru kategori: ").strip()
                        new_code = input("Masukkan kode baru kategori: ").strip()
                        new_description = input("Masukkan deskripsi baru kategori: ").strip()
                        if not new_name or not new_code or not new_description:
                            print("Nama, kode, dan deskripsi baru tidak boleh kosong!")
                        else:
                            edit_kategori(categories_id, new_name, new_code, new_description)
                    except ValueError:
                        print("ID kategori harus berupa angka.")
                else:
                    print("Maaf, hanya admin yang dapat mengedit kategori.")
            elif pilihan == 4:
                if role == 'admin':
                    try:
                        categories_id = int(input("Masukkan ID kategori yang ingin dihapus: "))
                        hapus_kategori(categories_id)
                    except ValueError:
                        print("ID kategori harus berupa angka.")
                else:
                    print("Maaf, hanya admin yang dapat menghapus kategori.")
            elif pilihan == 5:
                print("Anda Akan Kembali Ke Menu user/admin!!")
                if role == "admin":
                    Account.admin_access()
                else:
                    Account.user_access()
                return
            elif pilihan == 6:
                print("Anda Akan Kembali Ke Menu Login!!")
                Account.main()
                return
            elif pilihan == 7:
                print("Anda Akan Kembali Ke Menu Utama!!")
                menu()
                return
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("Masukkan angka untuk memilih opsi.")

if __name__ == "__main__":
    halaman_kategori()