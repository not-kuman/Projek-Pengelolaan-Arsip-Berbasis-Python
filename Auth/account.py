import sqlite3
import hashlib
import re

def create_db_connection():
    return sqlite3.connect('DB_Arsip.db')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_users_table():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS account (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
    )''')
    conn.commit()
    conn.close()

def validate_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

class Account:
    def login():
        create_users_table()
        conn = create_db_connection()
        cursor = conn.cursor()
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        
        if not username or not password:
            print("Username dan password tidak boleh kosong!")
            conn.close()
            return None
        hashed_password = hash_password(password)
        cursor.execute("SELECT role FROM account WHERE username = ? AND password = ?",  (username, hashed_password))
        user = cursor.fetchone()
        
        if user:
            print(f"Selamat Datang {username}.")
            print(f"Anda adalah {user[0]}.")
            conn.close()
            return user[0]
        else:
            print("Username atau password salah!")
            conn.close()
            return None

    def create_account():
        create_users_table()
        conn = create_db_connection()
        cursor = conn.cursor()
        username = input("Masukkan username baru: ")
        email = input("Masukkan email: ")
        
        if not validate_email(email):
            print("Error: Format email tidak valid!")
            conn.close()
            return
        cursor.execute("SELECT * FROM account WHERE username = ? OR email = ?", (username, email))
        
        if cursor.fetchone():
            print("Username atau email sudah terdaftar.")
            conn.close()
            return
            
        password = input("Masukkan password baru: ")
        if len(password) < 6:
            print("Password harus lebih dari 6 karakter!")
            conn.close()
            return
            
        role = input("Masukkan peran (admin/user): ").lower()
        if role not in ["admin", "user"]:
            print("Peran tidak valid. Hanya 'admin' atau 'user'.")
            conn.close()
            return
            
        try:
            hashed_password = hash_password(password)
            cursor.execute("""
                INSERT INTO account (username, email, password, role) 
                VALUES (?, ?, ?, ?)""", 
                (username, email, hashed_password, role))
            conn.commit()
            print(f"Akun {username} berhasil dibuat sebagai {role}.")
        except sqlite3.IntegrityError as e:
            print(f"Terjadi kesalahan: {e}")
        finally:
            conn.close()

    def edit_account():
        create_users_table()
        conn = create_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT account_id, username, email, role FROM account")
        accounts = cursor.fetchall()
        
        if not accounts:
            print("Tidak ada akun yang terdaftar.")
            conn.close()
            return
            
        for account in accounts:
            print(f"ID: {account[0]}, Username: {account[1]}, Email: {account[2]}, Role: {account[3]}")
            
        account_id = input("Masukkan ID akun yang ingin diedit: ")
        cursor.execute("SELECT * FROM account WHERE account_id = ?", (account_id,))
        user = cursor.fetchone()
        
        if not user:
            print("ID akun tidak ditemukan.")
            conn.close()
            return
            
        print(f"Data Akun: Username: {user[1]}, Email: {user[2]}, Role: {user[4]}")
        
        new_email = input("Masukkan email baru (Enter untuk tidak mengubah): ")
        if new_email:
            if not validate_email(new_email):
                print("Error: Format email tidak valid!")
                conn.close()
                return
                
            cursor.execute("SELECT * FROM account WHERE email = ? AND account_id != ?", (new_email, account_id))
            if cursor.fetchone():
                print("Email sudah terdaftar.")
                conn.close()
                return
                
        new_password = input("Masukkan password baru (Enter untuk tidak mengubah): ")
        if new_password and len(new_password) < 6:
            print("Password harus lebih dari 6 karakter!")
            conn.close()
            return
            
        new_role = input("Masukkan peran baru (admin/user) atau Enter: ").lower()
        if new_role and new_role not in ["admin", "user"]:
            print("Peran tidak valid.")
            conn.close()
            return
            
        try:
            cursor.execute("""
                UPDATE account 
                SET email = COALESCE(?, email),
                    password = COALESCE(?, password),
                    role = COALESCE(?, role)
                WHERE account_id = ?""",
                (new_email if new_email else None, hash_password(new_password) if new_password else None, new_role if new_role else None, account_id))
            conn.commit()
            print("Akun berhasil diperbarui!")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan: {e}")
        finally:
            conn.close()

    def delete_account():
        create_users_table()
        conn = create_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT account_id, username, email, role FROM account")
        accounts = cursor.fetchall()
        
        if not accounts:
            print("Tidak ada akun yang terdaftar.")
            conn.close()
            return
            
        for account in accounts:
            print(f"ID: {account[0]}, Username: {account[1]}, Email: {account[2]}, Role: {account[3]}")
            
        account_id = input("Masukkan ID akun yang ingin dihapus: ")
        cursor.execute("SELECT * FROM account WHERE account_id = ?", (account_id,))
        user = cursor.fetchone()
        
        if not user:
            print("ID akun tidak ditemukan.")
            conn.close()
            return
            
        if input("Konfirmasi penghapusan (y/n): ").lower() == 'y':
            try:
                cursor.execute("DELETE FROM account WHERE account_id = ?", (account_id,))
                conn.commit()
                print("Akun berhasil dihapus!")
            except sqlite3.Error as e:
                print(f"Terjadi kesalahan: {e}")
        else:
            print("Penghapusan dibatalkan.")
            
        conn.close()

    def manage_user():
        create_users_table()
        conn = create_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT account_id, username, email, role FROM account")
        users = cursor.fetchall()
        
        if users:
            print("\nDaftar Pengguna:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
        else:
            print("Tidak ada pengguna yang terdaftar.")
            
        conn.close()

    def admin_access():
        from Data.archives import halaman_arsip
        from Data.category import halaman_kategori
        from Data.logs import log_action
        from Data.surat import letter_page
        from Data.tindak_lanjut import  letter_followup
        from menu import menu
        username = "admin"
        while True:
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
            pilihan = input("Pilih opsi (1-10): ")
            if pilihan == 1:
                Account.create_account()
                log_action("Created a new account", username)
            elif pilihan == 2:
                Account.edit_account()
                log_action("Edited an account", username)
            elif pilihan == 3:
                Account.delete_account()
                log_action("Deleted an account", username)
            elif pilihan == 4:
                Account.manage_user()
                log_action("Managed user accounts", username)
            elif pilihan == 5:
                halaman_arsip()
                log_action("Managed archives", username)
                break
            elif pilihan == 6:
                halaman_kategori()
                log_action("Managed categories", username)
                break
            elif pilihan == 7:
                letter_page()
                log_action("Managed surat", username)
                break
            elif pilihan == 8:
                letter_followup()
                log_action("Managed tindak lanjut", username)
                break
            elif pilihan == 9:
                print("\n--- Logs ---")
                try:
                    with open("logs.txt", "r") as log_file:
                        print(log_file.read())
                except FileNotFoundError:
                    print("No logs found.")
            elif pilihan == 10:
                print("Kembali ke Menu Utama...")
                menu()
                break
            else:
                print("Opsi tidak valid. Silakan pilih lagi.")

    def user_access():
        from Data.archives import halaman_arsip
        from Data.category import halaman_kategori
        from Data.surat import letter_page
        from Data.logs import log_action
        from menu import menu
        username = "user"
        while True:
            print("\nSelamat Datang di Panel User")
            print("1. Buat Akun Baru")
            print("2. Kelola Arsip")
            print("3. Kelola Kategori")
            print("4. Kelola Surat")
            print("5. Kembali ke Menu Utama")
            pilihan = int(input("Pilihan menu: "))
            if pilihan == 1:
                Account.create_account()
                log_action("Created a new account", username)
            elif pilihan == 2:
                halaman_arsip()
                log_action("Managed archives", username)
                break
            elif pilihan ==3:
                halaman_kategori()
                log_action("Managed categories", username)
                break
            elif pilihan == 4:
                letter_page()
                log_action("Managed surat", username)
                break
            elif pilihan == 5:
                print("Kembali ke Menu Login...")
                Account.main()
                break
            else:
                print("Opsi tidak valid. Silakan pilih lagi.")

    def main():
        from menu import menu
        print("\n Selamat Datang Pengguna, Silahkan Pilih Opsi dibawah Ini !!.")
        while True:
            print("1. Buat Akun Baru")
            print("2. Login")
            print("3. Keluar ke Menu Utama")
            pilihan = input(int("Pilih opsi (1, 2, 3): "))
            
            if pilihan ==1:
                Account.create_account()
            elif pilihan ==2:
                role = Account.login()
                if role == "admin":
                    Account.admin_access()
                elif role == "user":
                    Account.user_access()
                else:
                    print("Login gagal. Silakan coba lagi.")
            elif pilihan ==3:
                print("Kembali ke Menu Utama...")
                menu()
                break
            else:
                print("Opsi tidak valid. Harap pilih 1, 2, atau 3.")

    if __name__ == "__main__":
        main()
