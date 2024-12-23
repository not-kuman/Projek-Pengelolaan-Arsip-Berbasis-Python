import sqlite3
import datetime
from Auth.account import Account
from mainmenu import menu

def create_table():
    """
    Membuat tabel 'tindak_lanjut' jika belum ada.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tindak_lanjut (
                tindak_lanjut_id INTEGER PRIMARY KEY,
                surat_id INTEGER,
                tindakan TEXT NOT NULL,
                tanggal_tindak DATE NOT NULL,
                FOREIGN KEY(surat_id) REFERENCES surat(surat_id)
            )
        ''')
        conn.commit()
        print("Tabel tindak_lanjut berhasil dibuat atau sudah ada.")
    except sqlite3.Error as e:
        print(f"Error saat membuat tabel: {e}")
    finally:
        conn.close()

def tambah_tindak_lanjut():
    """
    Menambahkan data tindak lanjut ke tabel.
    """
    create_table()  # Memastikan tabel sudah dibuat
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()

        tindak_lanjut_id = int(input("Masukkan tindak lanjut ID: "))
        surat_id = int(input("Masukkan surat ID: "))
        tindakan = input("Masukkan tindakan: ")
        tanggal_tindak = input("Masukkan tanggal tindak (format YYYY-MM-DD): ")

        # Validasi format tanggal
        try:
            datetime.datetime.strptime(tanggal_tindak, '%Y-%m-%d')
        except ValueError:
            print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
            return

        cursor.execute('''
            INSERT INTO tindak_lanjut (tindak_lanjut_id, surat_id, tindakan, tanggal_tindak) 
            VALUES (?, ?, ?, ?)
        ''', (tindak_lanjut_id, surat_id, tindakan, tanggal_tindak))
        conn.commit()
        print("Data tindak lanjut berhasil disimpan!")

    except sqlite3.Error as e:
        print(f"Terjadi kesalahan pada database: {e}")
    except ValueError:
        print("Input tidak valid. Pastikan data sesuai dengan tipe yang diminta.")
    finally:
        conn.close()

def tindak_lanjut():
    """
    Menu utama untuk pengelolaan tindak lanjut.
    """
    while True:
        print("\n=== Halaman Utama ===")
        print("1. Login")
        print("2. Tambah Tindak Lanjut")
        print("3. Keluar")
        choice = input("Pilih opsi (1/2/3): ")

        if choice == "1":
            role = Account
            if role == "admin":
                Account.admin_access()
            elif role == "user":
                print("Anda tidak memiliki akses ke halaman admin.")
            else:
                print("Login gagal. Silakan coba lagi.")

        elif choice == "2":
            tambah_tindak_lanjut()

        elif choice == "3":
            print("Keluar dari menu. Kembali ke Menu Awal!")
            menu()
            break

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    tindak_lanjut()
