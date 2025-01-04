import sqlite3
import datetime
from Auth.account import Account
from mainmenu import menu

DATABASE_NAME = 'DB_Arsip.db'


class LetterFollowUpManager:
    def __init__(self):
        self.account = Account()
        self.role = self.account.login()

    def create_table(self):
        """
        Membuat tabel 'letter_followup' jika belum ada.
        """
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS letter_followup (
                    follow_up_id INTEGER PRIMARY KEY,
                    letter_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    action_date DATE NOT NULL,
                    status TEXT CHECK(status IN ('Pending', 'Completed')) DEFAULT 'Pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(letter_id) REFERENCES letter(letter_id)
                )
            ''')
            conn.commit()
            print("Tabel 'letter_followup' berhasil dibuat atau sudah ada.")
        except sqlite3.Error as e:
            print(f"Error saat membuat tabel: {e}")
        finally:
            conn.close()

    def add_letter_followup(self):
        """
        Menambahkan data tindak lanjut ke tabel 'letter_followup'.
        """
        self.create_table()
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            print("\n=== Tambah Tindak Lanjut ===")
            follow_up_id = int(input("Masukkan ID tindak lanjut: "))
            letter_id = int(input("Masukkan ID surat: "))
            action = input("Masukkan tindakan: ")
            action_date = input("Masukkan tanggal tindakan (format YYYY-MM-DD): ")
            try:
                datetime.datetime.strptime(action_date, '%Y-%m-%d')
            except ValueError:
                print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
                return
            status = input("Masukkan status (Pending/Completed) [default: Pending]: ").capitalize()
            if status not in ['Pending', 'Completed', '']:
                print("Status tidak valid. Gunakan 'Pending' atau 'Completed'.")
                return
            status = status if status else 'Pending'
            cursor.execute('''
                INSERT INTO letter_followup (follow_up_id, letter_id, action, action_date, status) 
                VALUES (?, ?, ?, ?, ?)
            ''', (follow_up_id, letter_id, action, action_date, status))
            conn.commit()
            print("Data tindak lanjut berhasil disimpan!")
        except sqlite3.IntegrityError:
            print("Error: ID tindak lanjut atau ID surat tidak valid atau sudah ada.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan pada database: {e}")
        except ValueError:
            print("Input tidak valid. Pastikan data sesuai dengan tipe yang diminta.")
        finally:
            conn.close()

    def show_letter_followup(self):
        """
        Menampilkan semua data tindak lanjut di tabel 'letter_followup'.
        """
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            print("\n=== Data Tindak Lanjut ===")
            cursor.execute('SELECT * FROM letter_followup')
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"ID: {row[0]}, Letter ID: {row[1]}, Action: {row[2]}, Date: {row[3]}, Status: {row[4]}, Created: {row[5]}, Updated: {row[6]}")
            else:
                print("Belum ada data tindak lanjut.")
        except sqlite3.Error as e:
            print(f"Terjadi kesalahan pada database: {e}")
        finally:
            conn.close()

    def letter_followup(self):
        """
        Menu utama untuk pengelolaan tindak lanjut.
        """
        if self.role is None:
            print("Silakan login terlebih dahulu")
            return
        while True:
            print("\n=== Halaman Utama Tindak Lanjut ===")
            print("1. Tambah Tindak Lanjut")
            print("2. Tampilkan Semua Tindak Lanjut")
            print("3. Kembali ke Menu admin")
            print("4. Kembali ke Menu Login")
            print("5. Kembali ke Menu Utama")
            try:
                pilihan = int(input("Masukkan pilihan: "))
            except ValueError:
                print("Pilihan tidak valid. Silakan masukkan angka.")
                continue

            if pilihan == 1:
                self.add_letter_followup()
            elif pilihan == 2:
                self.show_letter_followup()
            elif pilihan == 3:
                print("Anda Akan Kembali Ke Menu admin!!")
                self.account.admin_access()
                return
            elif pilihan == 4:
                print("Anda Akan Kembali Ke Menu Login!!")
                self.account.main()
                return
            elif pilihan == 5:
                print("Anda Akan Kembali Ke Menu Utama!!")
                menu()
                return
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    manager = LetterFollowUpManager()
    manager.letter_followup()
