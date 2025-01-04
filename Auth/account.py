import sqlite3
import hashlib
import re
from functools import wraps

class DatabaseManager:
    DATABASE_NAME = 'DB_Arsip.db'
    
    @classmethod
    def get_connection(cls):
        return sqlite3.connect(cls.DATABASE_NAME)
    
    @classmethod
    def initialize_database(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS account (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
            )''')
            conn.commit()

class Account:
    def __init__(self):
        self.username = None
        self.role = None
        DatabaseManager.initialize_database()
    
    @staticmethod
    def validate_email(email):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Method untuk proses login"""
        try:
            with DatabaseManager.get_connection() as conn:
                cursor = conn.cursor()
                username = input("Username: ").strip()
                password = self.hash_password(input("Password: ").strip())
                
                cursor.execute('SELECT role FROM account WHERE username = ? AND password = ?', 
                             (username, password))
                result = cursor.fetchone()
                
                if result:
                    self.username = username
                    self.role = result[0]
                    print(f"\nLogin berhasil sebagai {self.role}")
                    return self.role
                else:
                    print("\nUsername atau password salah")
                    return None
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan database: {e}")
            return None
    @classmethod
    def create_account(cls):
        try:
            with DatabaseManager.get_connection() as conn:
                cursor = conn.cursor()
                
                username = input("Masukkan username baru: ").strip()
                if not username:
                    print("Username tidak boleh kosong!")
                    return
                
                email = input("Masukkan email: ").strip()
                if not cls.validate_email(email):
                    print("Error: Format email tidak valid!")
                    return
                
                password = input("Masukkan password baru: ").strip()
                if len(password) < 6:
                    print("Password harus lebih dari 6 karakter!")
                    return
                
                role = input("Masukkan peran (admin/user): ").lower().strip()
                if role not in ["admin", "user"]:
                    print("Peran tidak valid. Hanya 'admin' atau 'user'.")
                    return
                
                cursor.execute("""
                    INSERT INTO account (username, email, password, role) 
                    VALUES (?, ?, ?, ?)
                    """, (username, email, cls.hash_password(password), role))
                conn.commit()
                print(f"Akun {username} berhasil dibuat sebagai {role}.")
                
        except sqlite3.IntegrityError:
            print("Username atau email sudah terdaftar.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan database: {e}")
    
    def admin_access(self):
        while True:
            from Data.archived import halaman_arsip
            from Data.category import halaman_kategori
            from Data.logs import log_action
            from Data.logs import add_log_to_file
            from Data.surat import letter_page
            from Data.tindak_lanjut import letter_followup
            try:
                print("\nSelamat Datang di Panel Admin")
                print("1. Buat Akun Baru")
                print("2. Edit Akun")
                print("3. Hapus Akun")
                print("4. Kelola Pengguna")
                print("5. Kelola Arsip")
                print("6. Kelola Kategori")
                print("7. Kelola Surat")
                print("8. Kelola Tindak Lanjut")
                print("9. Lihat Logs")
                print("10. Kembali ke Menu Utama")
                
                pilihan = int(input("Masukkan pilihan: "))  # Fixed input handling
                
                if pilihan == 1:
                    self.create_account()
                    self.log_action("Create")
                elif pilihan == 2:
                    self.edit_account()
                    self.log_action("Update")
                elif pilihan == 3:
                    self.delete_account()
                    self.log_action("Delete")
                elif pilihan == 4:
                    self.manage_user()
                    self.log_action("Update")
                elif pilihan == 5:
                    halaman_arsip()
                    self.log_action("Update")
                    break
                elif pilihan == 6:
                    halaman_kategori()
                    self.log_action("Update")
                    break
                elif pilihan == 7:
                    letter_page()
                    self.log_action("Update")
                    break
                elif pilihan == 8:
                    letter_followup()
                    self.log_action("Update")
                    break
                elif pilihan == 9:
                    add_log_to_file()
                    self.log_action("View")
                elif pilihan == 10:
                    print("Kembali ke Menu Utama...")
                    from mainmenu import menu
                    menu()
                    break
                else:
                    print("Opsi tidak valid. Harap pilih 1-10.")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
    
    def user_access(self):
        while True:
            from Data.category import halaman_kategori
            from Data.surat import letter_page
            from Data.logs import log_action
            try:
                print("\nSelamat Datang di Panel Pengguna")
                print("1. Lihat Arsip")
                print("2. Lihat Kategori")
                print("3. Lihat Surat")
                print("4. Kembali ke Menu Utama")
                
                pilihan = int(input("Masukkan pilihan: "))  # Fixed input handling
                
                if pilihan == 1:
                    from Data.archived import halaman_arsip
                    halaman_arsip()
                    self.log_action("View")
                elif pilihan == 2:
                    halaman_kategori()
                    self.log_action("View")
                elif pilihan == 3:
                    letter_page()
                    self.log_action("View")
                elif pilihan == 4:
                    print("Kembali ke Menu Utama...")
                    from mainmenu import menu
                    menu()
                    break
                else:
                    print("Opsi tidak valid. Harap pilih 1-4.")
                    
            except ValueError:
                print("Masukkan angka yang valid!")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
    
    @classmethod
    def main(cls):
        print("\nSelamat Datang Pengguna, Silahkan Pilih Opsi di bawah Ini!")
        account = cls()
        
        while True:
            try:
                print("\n1. Buat Akun Baru")
                print("2. Login")
                print("3. Keluar ke Menu Utama")
                
                pilihan = int(input("Masukkan pilihan: "))  # Fixed input handling
                
                if pilihan == 1:
                    cls.create_account()
                elif pilihan == 2:
                    role = account.login()
                    if role == "admin":
                        account.admin_access()
                        break
                    elif role == "user":
                        account.user_access()
                        break
                elif pilihan == 3:
                    print("Kembali ke Menu Utama...")
                    from mainmenu import menu
                    menu()
                    break
                else:
                    print("Opsi tidak valid. Harap pilih 1, 2, atau 3.")
                    
            except ValueError:
                print("Masukkan angka yang valid!")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    Account.main()