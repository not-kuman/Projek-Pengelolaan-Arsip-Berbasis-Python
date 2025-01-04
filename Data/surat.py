import sqlite3
from datetime import datetime
from Auth.account import Account
from mainmenu import menu

class LetterManager:
    def __init__(self):
        self.account = Account()
        self.role = self.account.login()
        self.account_id = self.account.login()

    def create_db_connection(self):
        """Helper function to create and return a database connection."""
        return sqlite3.connect('DB_Arsip.db')

    def create_letter_table(self):
        """Membuat tabel surat jika belum ada."""
        conn = self.create_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS letter (
                letter_id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                letter_content VARCHAR,
                sender VARCHAR,
                content TEXT,
                date_received DATE,
                status TEXT CHECK(status IN ('in process', 'completed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES account(account_id)
            )
        ''')
        conn.commit()
        conn.close()

    def add_letter(self, letter_content, sender, content, date_received, status):
        """Menambahkan surat baru ke tabel letter."""
        conn = self.create_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO letter (account_id, letter_content, sender, content, date_received, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.account_id, letter_content, sender, content, date_received, status))
            conn.commit()
            print("Surat berhasil ditambahkan.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat menambahkan surat: {e}")
        finally:
            conn.close()

    def view_letters(self):
        """Melihat semua surat yang ada di tabel letter."""
        conn = self.create_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM letter WHERE account_id = ?', (self.account_id,))
        letters = cursor.fetchall()
        if letters:
            print("\nDaftar Surat:")
            for letter in letters:
                print(f"ID: {letter[0]}, Account ID: {letter[1]}, Konten: {letter[2]}, Pengirim: {letter[3]}, "
                      f"Isi: {letter[4]}, Tanggal Diterima: {letter[5]}, Status: {letter[6]}, "
                      f"Dibuat: {letter[7]}, Diperbarui: {letter[8]}")
        else:
            print("Tidak ada surat yang ditemukan.")
        conn.close()

    def edit_letter(self, letter_id, letter_content, sender, content, date_received, status):
        """Mengedit surat berdasarkan ID."""
        conn = self.create_db_connection()
        cursor = conn.cursor()
        update_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            cursor.execute('''
                UPDATE letter
                SET letter_content = ?, sender = ?, content = ?, 
                    date_received = ?, status = ?, update_at = ?
                WHERE letter_id = ? AND account_id = ?
            ''', (letter_content, sender, content, date_received, status, update_at, letter_id, self.account_id))
            if cursor.rowcount > 0:
                print(f"Surat dengan ID {letter_id} berhasil diperbarui.")
            else:
                print(f"Surat dengan ID {letter_id} tidak ditemukan atau Anda tidak memiliki akses.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat memperbarui surat: {e}")
        finally:
            conn.commit()
            conn.close()

    def delete_letter(self, letter_id):
        """Menghapus surat berdasarkan ID."""
        conn = self.create_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM letter WHERE letter_id = ? AND account_id = ?', (letter_id, self.account_id))
            if cursor.rowcount > 0:
                print(f"Surat dengan ID {letter_id} berhasil dihapus.")
            else:
                print(f"Surat dengan ID {letter_id} tidak ditemukan atau Anda tidak memiliki akses.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan saat menghapus surat: {e}")
        finally:
            conn.commit()
            conn.close()

    def letter_page(self):
        """Menampilkan halaman pengelolaan surat."""
        self.create_letter_table()
        if self.role is None:
            print("Silakan login terlebih dahulu.")
            return
        while True:
            print("\n=== Pengelolaan Surat ===")
            print("1. Tambah Surat")
            print("2. Lihat Surat")
            if self.role == "admin":
                print("3. Edit Surat")
                print("4. Hapus Surat")
            print("5. Kembali ke Menu user/admin")
            print("6. Kembali ke Menu Login")
            print("7. Kembali ke Menu Utama")
            try:
                pilihan = int(input("Masukkan pilihan: "))
            except ValueError:
                print("Pilihan tidak valid. Harap masukkan angka.")
                continue

            if pilihan == 1:
                letter_content = input("Masukkan konten surat: ")
                sender = input("Masukkan pengirim: ")
                content = input("Masukkan isi surat: ")
                date_received = input("Masukkan tanggal diterima (YYYY-MM-DD): ")
                try:
                    date_received = datetime.strptime(date_received, "%Y-%m-%d").date()
                except ValueError:
                    print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
                    continue
                status = input("Masukkan status (in process/completed): ")
                if status not in ['in process', 'completed']:
                    print("Status tidak valid.")
                    continue
                self.add_letter(letter_content, sender, content, date_received, status)
            elif pilihan == 2:
                self.view_letters()
            elif self.role == "admin" and pilihan == 3:
                try:
                    letter_id = int(input("Masukkan ID surat yang ingin diedit: "))
                    letter_content = input("Masukkan konten baru surat: ")
                    sender = input("Masukkan pengirim baru: ")
                    content = input("Masukkan isi baru surat: ")
                    date_received = input("Masukkan tanggal diterima baru (YYYY-MM-DD): ")
                    try:
                        date_received = datetime.strptime(date_received, "%Y-%m-%d").date()
                    except ValueError:
                        print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
                        continue
                    status = input("Masukkan status baru (in process/completed): ")
                    if status not in ['in process', 'completed']:
                        print("Status tidak valid.")
                        continue
                    self.edit_letter(letter_id, letter_content, sender, content, date_received, status)
                except ValueError:
                    print("ID surat harus berupa angka.")
            elif self.role == "admin" and pilihan == 4:
                try:
                    letter_id = int(input("Masukkan ID surat yang ingin dihapus: "))
                    self.delete_letter(letter_id)
                except ValueError:
                    print("ID surat harus berupa angka.")
            elif pilihan == 5:
                print("Anda Akan Kembali Ke Menu user/admin!!")
                if self.role == "admin":
                    self.account.admin_access()
                else:
                    self.account.user_access()
                return
            elif pilihan == 6:
                print("Anda Akan Kembali Ke Menu Login!!")
                self.account.main()
                return
            elif pilihan == 7:
                print("Anda Akan Kembali Ke Menu Utama!!")
                menu()
                return
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    app = LetterManager()
    app.letter_page()
