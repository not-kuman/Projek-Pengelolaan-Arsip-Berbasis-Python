import sqlite3
from datetime import datetime
from Auth.account import Account
from mainmenu import menu

DATABASE_NAME = 'DB_Arsip.db'

class ArsipManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()
        self.buat_tabel_arsip()  # Membuat tabel saat inisialisasi
        self.account = Account()
        self.role = None

    def initialize_system(self):
        """Menginisialisasi sistem dengan login"""
        self.role = self.account.login()
        if self.role:
            self.halaman_arsip()
        else:
            print("Login gagal. Silakan coba lagi.")

    def buat_tabel_arsip(self):
        """Membuat tabel archives jika belum ada."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS archives (
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
        self.conn.commit()


    def handle_tambah_arsip(self):
        """Handle penambahan arsip dengan validasi input"""
        try:
            category_id = int(input("Masukkan ID kategori: "))
            account_id = int(input("Masukkan ID akun: "))
            title = input("Masukkan judul arsip: ").strip()
            description = input("Masukkan deskripsi arsip: ").strip()
            file_path = input("Masukkan path file arsip: ").strip()
            
            if not title or not description or not file_path:
                print("Judul, deskripsi, dan file path tidak boleh kosong!")
                return
                
            self.tambah_arsip(category_id, account_id, title, description, file_path)
        except ValueError:
            print("ID kategori dan ID akun harus berupa angka.")

    def handle_edit_arsip(self):
        """Handle edit arsip dengan validasi input"""
        try:
            archives_id = int(input("Masukkan ID arsip yang ingin diedit: "))
            new_title = input("Masukkan judul baru arsip: ").strip()
            new_description = input("Masukkan deskripsi baru arsip: ").strip()
            new_file_path = input("Masukkan path file baru arsip: ").strip()
            
            if not new_title or not new_description or not new_file_path:
                print("Judul, deskripsi, dan file path tidak boleh kosong!")
                return
                
            self.edit_arsip(archives_id, new_title, new_description, new_file_path)
        except ValueError:
            print("ID arsip harus berupa angka.")

    def handle_hapus_arsip(self):
        """Handle hapus arsip dengan validasi input"""
        try:
            archives_id = int(input("Masukkan ID arsip yang ingin dihapus: "))
            self.hapus_arsip(archives_id)
        except ValueError:
            print("ID arsip harus berupa angka.")

    def lihat_arsip(self):
        """Melihat semua arsip yang ada di tabel archives."""
        conn = self.create_db_connection()
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

    
 
    def halaman_arsip(self):
        """Menampilkan halaman arsip dengan mengecek role."""
        if self.role is None:
            print("Silakan login terlebih dahulu")
            return

        while True:
            try:
                print("\n--- Halaman Arsip ---")
                print("1. Tambah Arsip")
                print("2. Lihat Arsip")
                print("3. Edit Arsip")
                print("4. Hapus Arsip")
                print("5. Kembali ke Menu user/admin")
                print("6. Kembali ke Menu Login")
                print("7. Kembali ke Menu Utama")
                
                pilihan = int(input("Masukkan pilihan: "))

                if pilihan == 1:
                    self.handle_tambah_arsip()
                elif pilihan == 2:
                    self.lihat_arsip()
                elif pilihan == 3:
                    if self.role == 'admin':
                        self.handle_edit_arsip()
                    else:
                        print("Maaf, hanya admin yang dapat mengedit arsip.")
                elif pilihan == 4:
                    if self.role == 'admin':
                        self.handle_hapus_arsip()
                    else:
                        print("Maaf, hanya admin yang dapat menghapus arsip.")
                elif pilihan == 5:
                    print("Anda Akan Kembali Ke Menu user/admin!")
                    if self.role == "admin":
                        self.account.admin_access()
                    else:
                        self.account.user_access()
                    break
                elif pilihan == 6:
                    print("Anda Akan Kembali Ke Menu Login!")
                    Account.main()
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
    arsip_manager = ArsipManager()
    arsip_manager.initialize_system()