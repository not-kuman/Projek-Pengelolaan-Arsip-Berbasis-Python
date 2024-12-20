import sqlite3
import hashlib

def create_db_connection():
    return sqlite3.connect('DB_Arsip.db')
def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

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
import re  # Untuk validasi email

def validate_email(email):
    """Fungsi untuk memvalidasi format email."""
    if '@' not in email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True
class Account:
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
            print(f"Selamat Datang {username[0]}.")
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
        print("Buat akun baru.")
        username = input("Masukkan username baru: ")
        email = input("Masukkan email: ")
        if not validate_email(email):
            print("Error: Format email tidak valid! Harap masukkan email dengan benar (contoh: user@example.com).")
            conn.close()
            return 
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
                    print("Terjadi kesalahan: ", e)
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
            new_email = input("Masukkan email baru (atau tekan Enter untuk tidak mengubah): ")
            if new_email:
                if not validate_email(new_email):
                    print("Error: Format email tidak valid! Harap masukkan email dengan benar (contoh: user@example.com).")
                    conn.close()
                    return
                cursor.execute("SELECT * FROM users WHERE email = ?", (new_email,))
                if cursor.fetchone():
                    print("Email baru sudah terdaftar. Coba yang lain.")
                    conn.close()
                    return
            new_password = input("Masukkan password baru (atau tekan Enter untuk tidak mengubah): ")
            if new_password and len(new_password) < 6:
                print("Password harus lebih dari 6 karakter!")
                conn.close()
                return
            hashed_new_password = hash_password(new_password) if new_password else user[2]
            new_role = input("Masukkan peran baru (admin/user) atau tekan Enter untuk tidak mengubah: ").lower()
            if new_role and new_role not in ["admin", "user"]:
                print("Peran tidak valid. Peran harus 'admin' atau 'user'.")
                conn.close()
                return
            try:
                cursor.execute("""
                    UPDATE users 
                    SET email = ?, password = ?, role = ? 
                    WHERE username = ?""",
                    (
                        new_email if new_email else user[1],
                        hashed_new_password,
                        new_role if new_role else user[3],
                        username
                    )
                )
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
            print(f"Akun ditemukan: Username: {user[0]}, Email: {user[1]}, Role: {user[3]}")
            confirm = input("Apakah Anda yakin ingin menghapus akun ini? (y/n): ").lower()
            if confirm == "y":
                try:
                    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                    conn.commit()
                    print(f"Akun {username} berhasil dihapus!")
                except sqlite3.Error as e:
                    print(f"Terjadi kesalahan saat menghapus akun: {e}")
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("Username tidak ditemukan.")
        conn.close()
    def manage_user():
        create_users_table()
        conn = create_db_connection()
        cursor = conn.cursor()
        print("\nKelola Pengguna:")
        cursor.execute("SELECT username, email, role FROM users")
        users = cursor.fetchall()
        if users:
            print("Daftar Pengguna:")
            for user in users:
                print(f"Username: {user[0]}, Email: {user[1]}, Role: {user[2]}")
        else:
            print("Tidak ada pengguna yang terdaftar.")
        conn.close()

    def admin_access():
        from Data.archives import halaman_arsip
        from Data.category import halaman_kategori
        from Data.logs import log_action
        from Data.surat import halaman_surat
        from Data.tindak_lanjut import tindak_lanjut
        from mainmenu import menu
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
            choice = input("Pilih opsi (1-10): ")
            if choice == "1":
                Account.create_account()
                log_action("Created a new account", username)
            elif choice == "2":
                Account.edit_account()
                log_action("Edited an account", username)
            elif choice == "3":
                Account.delete_account()
                log_action("Deleted an account", username)
            elif choice == "4":
                Account.manage_user()
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
                print("\n--- Logs ---")
                try:
                    with open("logs.txt", "r") as log_file:
                        print(log_file.read())
                except FileNotFoundError:
                    print("No logs found.")
            elif choice == "10":
                print("Kembali ke Menu Utama...")
                menu()
                break
            else:
                print("Opsi tidak valid. Silakan pilih lagi.")

    def user_faq():
        print("\nFAQ - Pertanyaan yang Sering Diajukan")
        print("1. Bagaimana cara mengelola arsip?")
        print("   - Pilih opsi 'Kelola Arsip' dari menu utama.")
        print("2. Bagaimana cara mengubah kategori?")
        print("   - Pilih opsi 'Kelola Kategori' dan sesuaikan sesuai kebutuhan.")
        print("3. Bagaimana cara mengelola surat?")
        print("   - Gunakan opsi 'Kelola Surat' untuk menambah atau menghapus surat.")

    def customer_service():
        print("\nCustomer Service")
        print("Untuk bantuan lebih lanjut, silakan hubungi:")
        print("- Email: example@arsipapp.com")
        print("- Telepon: 111-111-111-111")
        print("- Jam Operasional: Senin - Jumat, 08.00 - 17.00")

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
            print("5. FAQ")
            print("6. Customer Service")
            print("7. Kembali ke Menu Utama")
            choice = input("Pilih opsi (1-7): ")
            if choice == "1":
                Account.create_account()
            elif choice == "2":
                halaman_arsip()
            elif choice == "3":
                halaman_kategori()
            elif choice == "4":
                halaman_surat()
            elif choice == "5":
                Account.user_faq()
            elif choice == "6":
                Account.customer_service()
            elif choice == "7":
                print("Kembali ke Menu Login...")
                Account.main()
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
                Account.create_account()
            elif choice == "2":
                role = Account.login()
                if role == "admin":
                    Account.admin_access()
                elif role == "user":
                    Account.user_access()
                else:
                    print("Login gagal. Silakan coba lagi.")
            elif choice == "3":
                print("Kembali ke Menu Utama...")
                menu()
                break
            else:
                print("Opsi tidak valid. Harap pilih 1, 2, atau 3.")

    if __name__ == "__main__":
        main()
