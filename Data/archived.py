import sqlite3
from datetime import datetime
from Auth.account import Account

account = Account()
role = account.login()

def create_db_connection():
    """Helper function to create and return a database connection."""
    return sqlite3.connect('DB_Arsip.db')

def buat_tabel_arsip():
    """Membuat tabel archives jika belum ada."""
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS archives (
                       archives_id INTEGER PRIMARY KEY,
                       category_id INTEGER,
                       account_id INTEGER,
                       title TEXT,
                       description TEXT,
                       file_path TEXT,
                       created_at TIMESTAMP,
                       updated_at TIMESTAMP,
                       FOREIGN KEY (category_id) REFERENCES categories(categories_id),
                       FOREIGN KEY (account_id) REFERENCES account(account_id))''')
    conn.commit()
    conn.close()

def tambah_arsip(category_id, account_id, title, description, file_path):
    """Menambahkan arsip baru ke tabel archives."""
    conn = create_db_connection()
    cursor = conn.cursor()
    created_at = updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        cursor.execute('''INSERT INTO archives (category_id, account_id, title, description, file_path, created_at, updated_at)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                          (category_id, account_id, title, description, file_path, created_at, updated_at))
        conn.commit()
        print("Arsip berhasil ditambahkan.")
    except sqlite3.IntegrityError as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        conn.close()

def lihat_arsip():
    """Melihat semua arsip yang ada di tabel archives."""
    conn = create_db_connection()
    cursor = conn.cursor()

    cursor.execute('''SELECT a.archives_id, a.title, a.description, a.file_path, a.created_at, a.updated_at, c.categories_name, acc.username
                      FROM archives a
                      JOIN categories c ON a.category_id = c.categories_id
                      JOIN account acc ON a.account_id = acc.account_id''')
    rows = cursor.fetchall()

    if rows:
        print("\nDaftar Arsip:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Description: {row[2]}, File Path: {row[3]}, Created At: {row[4]}, Updated At: {row[5]}, Category: {row[6]}, Uploaded By: {row[7]}")
    else:
        print("Tidak ada arsip yang ditemukan.")

    conn.close()

def edit_arsip(archives_id, new_title, new_description, new_file_path):
    """Mengedit arsip berdasarkan ID."""
    conn = create_db_connection()
    cursor = conn.cursor()
    updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        cursor.execute('''UPDATE archives 
                          SET title = ?, description = ?, file_path = ?, updated_at = ?
                          WHERE archives_id = ?''', 
                          (new_title, new_description, new_file_path, updated_at, archives_id))

        if cursor.rowcount > 0:
            print(f"Arsip dengan ID {archives_id} berhasil diperbarui.")
        else:
            print(f"Arsip dengan ID {archives_id} tidak ditemukan.")
    finally:
        conn.commit()
        conn.close()

def hapus_arsip(archives_id):
    """Menghapus arsip berdasarkan ID."""
    conn = create_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM archives WHERE archives_id = ?', (archives_id,))

    if cursor.rowcount > 0:
        print(f"Arsip dengan ID {archives_id} berhasil dihapus.")
    else:
        print(f"Arsip dengan ID {archives_id} tidak ditemukan.")

    conn.commit()
    conn.close()

def halaman_arsip():
    """Menampilkan halaman arsip dengan mengecek role dari tabel account."""
    buat_tabel_arsip()
    from Auth.account import Account
    from mainmenu import menu

    global role
    if role is None:
        print("Silakan login terlebih dahulu")
        return

    while True:
        print("\n--- Halaman Arsip ---")
        print("1. Tambah Arsip")
        print("2. Lihat Arsip")
        print("3. Edit Arsip")
        print("4. Hapus Arsip")
        print("5. Kembali ke Menu user/admin")
        print("6. Kembali ke Menu Login")
        print("7. Kembali ke Menu Utama")

        try:
            pilihan = int(input("Masukkan pilihan: "))
            if pilihan == 1:
                if role == 'admin':
                    try:
                        category_id = int(input("Masukkan ID kategori: "))
                        account_id = int(input("Masukkan ID akun: "))
                        title = input("Masukkan judul arsip: ").strip()
                        description = input("Masukkan deskripsi arsip: ").strip()
                        file_path = input("Masukkan path file arsip: ").strip()

                        if not title or not description or not file_path:
                            print("Judul, deskripsi, dan file path tidak boleh kosong!")
                        else:
                            tambah_arsip(category_id, account_id, title, description, file_path)
                    except ValueError:
                        print("ID kategori dan ID akun harus berupa angka.")
                else:
                    print("Maaf, hanya admin yang dapat menambah arsip.")

            elif pilihan == 2:
                lihat_arsip()

            elif pilihan == 3:
                if role == 'admin':
                    try:
                        archives_id = int(input("Masukkan ID arsip yang ingin diedit: "))
                        new_title = input("Masukkan judul baru arsip: ").strip()
                        new_description = input("Masukkan deskripsi baru arsip: ").strip()
                        new_file_path = input("Masukkan path file baru arsip: ").strip()

                        if not new_title or not new_description or not new_file_path:
                            print("Judul, deskripsi, dan file path tidak boleh kosong!")
                        else:
                            edit_arsip(archives_id, new_title, new_description, new_file_path)
                    except ValueError:
                        print("ID arsip harus berupa angka.")
                else:
                    print("Maaf, hanya admin yang dapat mengedit arsip.")

            elif pilihan == 4:
                if role == 'admin':
                    try:
                        archives_id = int(input("Masukkan ID arsip yang ingin dihapus: "))
                        hapus_arsip(archives_id)
                    except ValueError:
                        print("ID arsip harus berupa angka.")
                else:
                    print("Maaf, hanya admin yang dapat menghapus arsip.")

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
    halaman_arsip()
