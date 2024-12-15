import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
def create_db_connection():
    """Helper function to create and return a database connection."""
    return sqlite3.connect('DB_Arsip.db')
def create_users_table():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
        )''')
    conn.commit()
    conn.close()

def login():
    create_users_table()
    conn = create_db_connection()
    cursor = conn.cursor()
    print("Selamat datang! Silakan login.")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    if not username or not password:
        print("Username dan password tidak boleh kosong!")
        conn.close()
        return None
    hashed_password = hash_password(password)
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    if user:
        print(f"Login berhasil! Anda adalah {user[0]}.")
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
    print("Buat akun baru.")
    username = input("Masukkan username baru: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print("Username sudah terdaftar. Coba username lain.")
    else:
        password = input("Masukkan password baru: ")
        if len(password) < 6:
            print("Password harus lebih dari 6 karakter!")
            conn.close()
            return
        hashed_password = hash_password(password)
        role = input("Masukkan peran (admin/user): ").lower()
        if role not in ["admin", "user"]:
            print("Peran tidak valid. Hanya 'admin' atau 'user' yang diperbolehkan.")
        else:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, role))
            conn.commit()
            print(f"Akun {username} berhasil dibuat sebagai {role}.")
    conn.close()

def edit_account():
    create_users_table()
    conn = create_db_connection()
    cursor = conn.cursor()
    print("\nEdit Akun:")
    username = input("Masukkan username yang ingin diedit: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        print(f"Data Akun: Username: {user[0]}, Role: {user[2]}")
        
        new_password = input("Masukkan password baru: ")
        if len(new_password) < 6:
            print("Password harus lebih dari 6 karakter!")
            conn.close()
            return
        hashed_new_password = hash_password(new_password)
        new_role = input("Masukkan peran baru (admin/user): ").lower()
        
        if new_role not in ["admin", "user"]:
            print("Peran tidak valid. Peran harus 'admin' atau 'user'.")
        else:
            cursor.execute("UPDATE users SET password = ?, role = ? WHERE username = ?", (hashed_new_password, new_role, username))
            conn.commit()
            print(f"Akun {username} berhasil diperbarui!")
    else:
        print("Username tidak ditemukan.")
    conn.close()

def delete_account():
    create_users_table()
    conn = create_db_connection()
    cursor = conn.cursor()
    print("\nHapus Akun:")
    username = input("Masukkan username yang ingin dihapus: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        print(f"Akun {username} berhasil dihapus!")
    else:
        print("Username tidak ditemukan.")
    conn.close()

def admin_access():
    from Data.archives import halaman_arsip
    from Data.category import halaman_kategori
    from Data.logs import log_action
    from Data.surat import halaman_surat
    from Data.tindak_lanjut import tindak_lanjut
    from mainmenu import menu
    username = "admin"  # Replace with actual logic if needed
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
        choice = input("Pilih opsi (1-10): ")
        if choice == "1":
            create_account()
            log_action("Created a new account", username)
        elif choice == "2":
            edit_account()
            log_action("Edited an account", username)
        elif choice == "3":
            delete_account()
            log_action("Deleted an account", username)
        elif choice == "4":
            print( " Menu Belum Tersedia")
            # manage_user() 
            log_action("Managed user accounts", username)
        elif choice == "5":
            halaman_arsip()
            log_action("Managed archives", username)
        elif choice == "6":
            halaman_kategori()
            log_action("Managed categories", username)
        elif choice == "7":
            halaman_surat()
            log_action("Managed surat", username)
        elif choice == "8":
            tindak_lanjut()
            log_action("Managed tindak lanjut", username)
        elif choice == "9":
            # Display logs
            print("\n--- Logs ---")
            try:
                with open("logs.txt", "r") as log_file:
                    print(log_file.read())  # Display all logs
            except FileNotFoundError:
                print("No logs found.")
        elif choice == "10":
            print("Kembali ke Menu Utama...")
            menu()
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")
def user_access():
    from Data.archives import halaman_arsip
    from Data.category import halaman_kategori
    from Data.surat import halaman_surat
    from mainmenu import menu

    while True:
        print("\nSelamat Datang di Panel User")
        print("1. Buat Akun Baru")
        print("2. Kelola Arsip")
        print("3. Kelola Kategori")
        print("4. Kelola Surat")
        print("5. Kembali ke Menu Utama")
        choice = input("Pilih opsi (1-10): ")
        if choice == "1":
            create_account()
        elif choice == "2":
            halaman_arsip()
        elif choice == "3":
            halaman_kategori()
        elif choice == "4":
            halaman_surat()
        elif choice == "5":
            print("Kembali ke Menu Utama...")
            menu()
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

def main():
    from mainmenu import menu
    print("\n Selamat Datang Pengguna, Silahkan Pilih Opsi dibawah Ini !!.")
    while True:
        print("1. Buat Akun Baru")
        print("2. Login")
        print("3. Keluar ke Menu Utama")
        choice = input("Pilih opsi (1, 2, 3): ")
        
        if choice == "1":
            create_account()
        elif choice == "2":
            role = login()
            if role == "admin":
                admin_access()
            elif role == "user":
                user_access()
        elif choice == "3":
            print("Kembali ke Menu Utama...")
            menu()
            break
        else:
            print("Opsi tidak valid. Harap pilih 1, 2, atau 3.")

if __name__ == "__main__":
    main()
