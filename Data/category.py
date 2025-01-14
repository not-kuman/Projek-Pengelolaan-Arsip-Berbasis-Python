import sqlite3
from datetime import datetime
from Auth.account import Account
from mainmenu import menu

DATABASE_NAME = 'DB_Arsip.db'

class KategoriManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()
        self.buat_tabel_kategori()  # Membuat tabel saat inisialisasi
        self.account = Account()
        self.role = None

    def initialize_system(self):
        """Menginisialisasi sistem dengan login"""
        self.role = self.account.login()
        if self.role:
            self.halaman_kategori()
        else:
            print("Login gagal. Silakan coba lagi.")

    def create_db_connection(self):
        """Helper function to create and return a database connection."""
        return sqlite3.connect(DATABASE_NAME)

    def get_user_role(self, username):
        """Mendapatkan role user dari tabel account."""
        conn = self.create_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM account WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            print("User tidak ditemukan")
            return None

    def buat_tabel_kategori(self):
        """Membuat tabel categories jika belum ada."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                               categories_id INTEGER PRIMARY KEY,
                               categories_name VARCHAR(100) UNIQUE,
                               categories_code VARCHAR(100) UNIQUE,
                               description TEXT,
                               created_at TIMESTAMP,
                               update_at TIMESTAMP)''')
        self.conn.commit()

    def tambah_kategori(self, categories_name, categories_code, description):
        """Menambahkan kategori baru ke tabel categories."""
        created_at = update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute('''INSERT INTO categories (categories_name, categories_code, description, created_at, update_at)
                                   VALUES (?, ?, ?, ?, ?)''', 
                                   (categories_name, categories_code, description, created_at, update_at))
            self.conn.commit()
            print("Kategori berhasil ditambahkan.")
        except sqlite3.IntegrityError:
            print(f"Kategori dengan nama '{categories_name}' atau kode '{categories_code}' sudah ada.")

    def lihat_kategori(self):
        """Melihat semua kategori yang ada di tabel categories."""
        self.cursor.execute('SELECT * FROM categories')
        rows = self.cursor.fetchall()
        if rows:
            print("\nDaftar Kategori:")
            for row in rows:
                print(f"ID: {row[0]}, Nama: {row[1]}, Kode: {row[2]}, Deskripsi: {row[3]}, Dibuat: {row[4]}, Diperbarui: {row[5]}")
        else:
            print("Tidak ada kategori yang ditemukan.")

    def edit_kategori(self, categories_id, new_name, new_code, new_description):
        """Mengedit kategori berdasarkan ID."""
        update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute('''UPDATE categories 
                                   SET categories_name = ?, categories_code = ?, description = ?, update_at = ?
                                   WHERE categories_id = ?''', 
                                   (new_name, new_code, new_description, update_at, categories_id))
            if self.cursor.rowcount > 0:
                print(f"Kategori dengan ID {categories_id} berhasil diperbarui.")
            else:
                print(f"Kategori dengan ID {categories_id} tidak ditemukan.")
        except sqlite3.IntegrityError:
            print("Nama atau kode kategori sudah digunakan.")
        finally:
            self.conn.commit()

    def hapus_kategori(self, categories_id):
        """Menghapus kategori berdasarkan ID."""
        self.cursor.execute('DELETE FROM categories WHERE categories_id = ?', (categories_id,))
        if self.cursor.rowcount > 0:
            print(f"Kategori dengan ID {categories_id} berhasil dihapus.")
        else:
            print(f"Kategori dengan ID {categories_id} tidak ditemukan.")
        self.conn.commit()

    def handle_tambah_kategori(self):
        """Handle penambahan kategori dengan validasi input"""
        categories_name = input("Masukkan nama kategori: ").strip()
        categories_code = input("Masukkan kode kategori: ").strip()
        description = input("Masukkan deskripsi kategori: ").strip()
        if not categories_name or not categories_code or not description:
            print("Nama, kode, dan deskripsi kategori tidak boleh kosong!")
        else:
            self.tambah_kategori(categories_name, categories_code, description)

    def handle_edit_kategori(self):
        """Handle edit kategori dengan validasi input"""
        try:
            categories_id = int(input("Masukkan ID kategori yang ingin diedit: "))
            new_name = input("Masukkan nama baru kategori: ").strip()
            new_code = input("Masukkan kode baru kategori: ").strip()
            new_description = input("Masukkan deskripsi baru kategori: ").strip()
            if not new_name or not new_code or not new_description:
                print("Nama, kode, dan deskripsi baru tidak boleh kosong!")
            else:
                self.edit_kategori(categories_id, new_name, new_code, new_description)
        except ValueError:
            print("ID kategori harus berupa angka.")

    def handle_hapus_kategori(self):
        """Handle hapus kategori dengan validasi input"""
        try:
            categories_id = int(input("Masukkan ID kategori yang ingin dihapus: "))
            self.hapus_kategori(categories_id)
        except ValueError:
            print("ID kategori harus berupa angka.")

    def halaman_kategori(self):
        """Menampilkan halaman kategori dengan mengecek role dari tabel account."""
        if self.role is None:
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
                    self.handle_tambah_kategori()
                elif pilihan == 2:
                    self.lihat_kategori()
                elif pilihan == 3:
                    if self.role == 'admin':
                        self.handle_edit_kategori()
                    else:
                        print("Maaf, hanya admin yang dapat mengedit kategori.")
                elif pilihan == 4:
                    if self.role == 'admin':
                        self.handle_hapus_kategori()
                    else:
                        print("Maaf, hanya admin yang dapat menghapus kategori.")
                elif pilihan == 5:
                    print("Anda Akan Kembali Ke Menu user/admin!")
                    if self.role == "admin":
                        self.account.admin_access()
                    else:
                        self.account.user_access()
                    break
                elif pilihan == 6:
                    print("Anda Akan Kembali Ke Menu Login!")
                    self.account.main()
                    break
                elif pilihan == 7:
                    print("Anda Akan Kembali Ke Menu Utama!")
                    menu()
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
            except ValueError:
                print("Masukkan angka untuk memilih opsi.")

if __name__ == "__main__":
    kategori_manager = KategoriManager()
    kategori_manager.initialize_system()
