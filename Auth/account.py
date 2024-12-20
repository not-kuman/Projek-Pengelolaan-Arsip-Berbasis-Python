import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_db_connection():
    return sqlite3.connect('DB_Arsip.db')

def create_users_table():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
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
    email = input("Masukkan email baru: ")
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    if cursor.fetchone():
        print("Username atau email sudah terdaftar. Coba yang lain.")
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
            try:
                cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", (username, email, hashed_password, role))
                conn.commit()
                print(f"Akun {username} berhasil dibuat sebagai {role}.")
            except sqlite3.IntegrityError as e:
                print(f"Terjadi kesalahan: {e}")
    conn.close()

def edit_account():
    create_users_table()
    conn = create_db_connection()
    cursor = conn.cursor()
    print("\nEdit Akun:")
    print("Daftar Akun:")
    cursor.execute("SELECT username, email, role FROM users")
    accounts = cursor.fetchall()
    if accounts:
        for account in accounts:
            print(f"Username: {account[0]}, Email: {account[1]}, Role: {account[2]}")
    else:
        print("Tidak ada akun yang terdaftar.")
        conn.close()
        return
    
    username = input("Masukkan username yang ingin diedit: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        print(f"Data Akun: Username: {user[0]}, Email: {user[1]}, Role: {user[3]}")
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
            try:
                cursor.execute("UPDATE users SET password = ?, role = ? WHERE username = ?", (hashed_new_password, new_role, username))
                conn.commit()
                print(f"Akun {username} berhasil diperbarui!")
            except sqlite3.Error as e:
                print(f"Terjadi kesalahan saat memperbarui akun: {e}")
    else:
        print("Username tidak ditemukan.")
    conn.close()

def delete_account():
    create_users_table()
    conn = create_db_connection()
    cursor = conn.cursor()
    print("\nHapus Akun:")
    print("Daftar Akun:")
    cursor.execute("SELECT username, email, role FROM users")
    accounts = cursor.fetchall()
    if accounts:
        for account in accounts:
            print(f"Username: {account[0]}, Email: {account[1]}, Role: {account[2]}")
    else:
        print("Tidak ada akun yang terdaftar.")
        conn.close()
        return

    username = input("Masukkan username yang ingin dihapus: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        try:
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            print(f"Akun {username} berhasil dihapus!")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat menghapus akun: {e}")
    else:
        print("Username tidak ditemukan.")
    conn.close()

def manage_user():
    create_users_table()
    conn = create_db_connection()
    cursor = conn.cursor()
    print("\nKelola Pengguna:")
    cursor.execute("SELECT username, email, role FROM users")
    accounts = cursor.fetchall()
    if accounts:
        print("Daftar Akun:")
        for account in accounts:
            print(f"Username: {account[0]}, Email: {account[1]}, Role: {account[2]}")
    else:
        print("Tidak ada akun yang terdaftar.")
    conn.close()

def admin_access():
    username = "admin"  # Replace with actual logic if needed
    while True:
        print("\nSelamat Datang di Panel Admin")
        print("1. Buat Akun Baru")
        print("2. Edit Akun")
        print("3. Hapus Akun")
        print("4. Kelola Pengguna")
        print("5. Kembali ke Menu Utama")
        choice = input("Pilih opsi (1-5): ")
        if choice == "1":
            create_account()
        elif choice == "2":
            edit_account()
        elif choice == "3":
            delete_account()
        elif choice == "4":
            manage_user()
        elif choice == "5":
            print("Kembali ke Menu Utama...")
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

def user_access():
    while True:
        print("\nSelamat Datang di Panel User")
        print("1. Buat Akun Baru")
        print("2. Kembali ke Menu Utama")
        choice = input("Pilih opsi (1-2): ")
        if choice == "1":
            create_account()
        elif choice == "2":
            print("Kembali ke Menu Utama...")
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

def main():
    while True:
        print("\nSelamat Datang!")
        print("1. Login")
        print("2. Keluar")
        choice = input("Pilih opsi (1-2): ")
        if choice == "1":
            role = login()
            if role == "admin":
                admin_access()
            elif role == "user":
                user_access()
        elif choice == "2":
            print("Keluar dari aplikasi. Sampai jumpa!")
            break
        else:
            print("Opsi tidak valid. Silakan pilih lagi.")

if __name__ == "__main__":
    main()
