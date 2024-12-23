import sqlite3
from datetime import datetime
from Auth.account import Account
from mainmenu import menu

def buat_tabel():
    """
    Membuat tabel 'surat' jika belum ada.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS surat (
                surat_id INTEGER PRIMARY KEY,
                nomor_surat VARCHAR(50),
                pengirim VARCHAR(100),
                isi_surat TEXT,
                tanggal_terima DATE,
                status TEXT CHECK(status IN ('proses', 'selesai'))
            )
        ''')
        conn.commit()
        print("Tabel surat berhasil dibuat atau sudah ada.")
    except sqlite3.Error as e:
        print(f"Error saat membuat tabel: {e}")
    finally:
        conn.close()

def tambah_surat(nomor_surat, pengirim, isi_surat, tanggal_terima, status):
    """
    Menambahkan surat baru ke tabel.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO surat (nomor_surat, pengirim, isi_surat, tanggal_terima, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (nomor_surat, pengirim, isi_surat, tanggal_terima, status))
        conn.commit()
        print("Surat berhasil ditambahkan.")
    except sqlite3.Error as e:
        print(f"Error saat menambahkan surat: {e}")
    finally:
        conn.close()

def lihat_surat():
    """
    Menampilkan semua surat dari tabel.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM surat')
        surat = cursor.fetchall()
        if surat:
            for s in surat:
                print(f"ID: {s[0]}, Nomor: {s[1]}, Pengirim: {s[2]}, Isi: {s[3]}, Tanggal: {s[4]}, Status: {s[5]}")
        else:
            print("Tidak ada surat yang ditemukan.")
    except sqlite3.Error as e:
        print(f"Error saat melihat surat: {e}")
    finally:
        conn.close()

def edit_surat(surat_id, new_nomor_surat, new_pengirim, new_isi_surat, new_tanggal_terima, new_status):
    """
    Mengedit surat berdasarkan ID.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE surat
            SET nomor_surat = ?, pengirim = ?, isi_surat = ?, tanggal_terima = ?, status = ?
            WHERE surat_id = ?
        ''', (new_nomor_surat, new_pengirim, new_isi_surat, new_tanggal_terima, new_status, surat_id))
        conn.commit()
        print("Surat berhasil diperbarui.")
    except sqlite3.Error as e:
        print(f"Error saat mengedit surat: {e}")
    finally:
        conn.close()

def hapus_surat(surat_id):
    """
    Menghapus surat berdasarkan ID.
    """
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM surat WHERE surat_id = ?', (surat_id,))
        conn.commit()
        print("Surat berhasil dihapus.")
    except sqlite3.Error as e:
        print(f"Error saat menghapus surat: {e}")
    finally:
        conn.close()

def halaman_surat(role):
    """
    Menu utama untuk manajemen surat.
    """
    while True:
        print("\n--- Halaman Surat ---")
        print("1. Tambah surat baru")
        print("2. Lihat semua surat")
        if role == "admin":
            print("3. Edit surat")
            print("4. Hapus surat")
            print("5. Kembali ke Menu Admin")
        else:
            print("3. Kembali ke Menu User")
        print("6. Kembali ke Menu Login")
        print("7. Kembali ke Menu Utama")

        pilihan = input("Masukkan pilihan: ")
        if pilihan == "1":
            nomor_surat = input("Masukkan nomor surat: ")
            pengirim = input("Masukkan pengirim surat: ")
            isi_surat = input("Masukkan isi surat: ")
            tanggal_terima = input("Masukkan tanggal terima (YYYY-MM-DD): ")
            try:
                tanggal_terima = datetime.strptime(tanggal_terima, "%Y-%m-%d").date()
            except ValueError:
                print("Format tanggal salah. Harap masukkan tanggal dalam format YYYY-MM-DD.")
                continue
            status = input("Masukkan status surat (proses/selesai): ")
            tambah_surat(nomor_surat, pengirim, isi_surat, tanggal_terima, status)
        elif pilihan == "2":
            lihat_surat()
        elif role == "admin" and pilihan == "3":
            surat_id = int(input("Masukkan ID surat: "))
            new_nomor_surat = input("Masukkan nomor surat baru: ")
            new_pengirim = input("Masukkan pengirim baru: ")
            new_isi_surat = input("Masukkan isi surat baru: ")
            new_tanggal_terima = input("Masukkan tanggal terima baru (YYYY-MM-DD): ")
            try:
                new_tanggal_terima = datetime.strptime(new_tanggal_terima, "%Y-%m-%d").date()
            except ValueError:
                print("Format tanggal salah. Harap masukkan tanggal dalam format YYYY-MM-DD.")
                continue
            new_status = input("Masukkan status surat baru (proses/selesai): ")
            edit_surat(surat_id, new_nomor_surat, new_pengirim, new_isi_surat, new_tanggal_terima, new_status)
        elif role == "admin" and pilihan == "4":
            surat_id = int(input("Masukkan ID surat: "))
            hapus_surat(surat_id)
        elif pilihan == "5":
            if role == "admin":
                print("Kembali ke Menu Admin.")
                Account.admin_access()
                break
            else:
                print("Kembali ke Menu User.")
                Account.user_access()
                break
        elif pilihan == "6":
            print("Kembali ke Menu Login.")
            menu()
            break
        elif pilihan == "7":
            print("Kembali ke Menu Utama.")
            menu()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    buat_tabel()
    role = "admin"  # Tentukan role secara manual untuk uji coba
    halaman_surat(role)
