import sqlite3
from datetime import datetime
role = None
def buat_tabel():
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS surat (
            surat_id INTEGER PRIMARY KEY,
            nomor_surat VARCHAR(50),
            pengirim VARCHAR(100),
            isi_surat TEXT,
            tanggal_terima DATE,
            status TEXT CHECK(status IN ('proses', 'selesai'))
        )''')
        conn.commit()
        print("Tabel surat berhasil dibuat atau sudah ada.")
    except sqlite3.Error as e:
        print(f"Error saat membuat tabel: {e}")
    finally:
        conn.close()

def tambah_surat(nomor_surat, pengirim, isi_surat, tanggal_terima, status):
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO surat (nomor_surat, pengirim, isi_surat, tanggal_terima, status)
                          VALUES (?, ?, ?, ?, ?)''', (nomor_surat, pengirim, isi_surat, tanggal_terima, status))
        conn.commit()
        print("Surat berhasil ditambahkan.")
    except sqlite3.Error as e:
        print(f"Error saat menambahkan surat: {e}")
    finally:
        conn.close()

def lihat_surat():
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM surat')
        surat = cursor.fetchall()
        if surat:
            for s in surat:
                print(s)
        else:
            print("Tidak ada surat yang ditemukan.")
    except sqlite3.Error as e:
        print(f"Error saat melihat surat: {e}")
    finally:
        conn.close()

def edit_surat(surat_id, new_nomor_surat, new_pengirim, new_isi_surat, new_tanggal_terima, new_status):
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE surat
                          SET nomor_surat = ?, pengirim = ?, isi_surat = ?, tanggal_terima = ?, status = ?
                          WHERE surat_id = ?''', 
                       (new_nomor_surat, new_pengirim, new_isi_surat, new_tanggal_terima, new_status, surat_id))
        conn.commit()
        print("Surat berhasil diperbarui.")
    except sqlite3.Error as e:
        print(f"Error saat mengedit surat: {e}")
    finally:
        conn.close()

def hapus_surat(surat_id):
    try:
        conn = sqlite3.connect('DB_Arsip.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM surat WHERE surat_id = ?''', (surat_id,))
        conn.commit()
        print("Surat berhasil dihapus.")
    except sqlite3.Error as e:
        print(f"Error saat menghapus surat: {e}")
    finally:
        conn.close()

def halaman_surat():
    role = Account 
    if role == "admin":
        from Auth.account import Account
        from mainmenu import menu
        print("\n--- Halaman Surat ---")
        print("1. Tambah surat baru")
        print("2. Lihat semua surat")
        print("3. Edit surat")
        print("4. Hapus surat")
        print("5. Kembali Ke menu user/admin")
        print("6. Kembali ke Menu Login")
        print("7. Kembali ke Menu Utama")

        try:
            pilihan = int(input("Masukkan pilihan: "))
            if pilihan == 1:
                nomor_surat = input("Masukkan nomor surat: ")
                pengirim = input("Masukkan pengirim surat: ")
                isi_surat = input("Masukkan isi surat: ")
                tanggal_terima = input("Masukkan tanggal terima (YYYY-MM-DD): ")
                # Periksa format tanggal
                try:
                    tanggal_terima = datetime.strptime(tanggal_terima, "%Y-%m-%d").date()
                except ValueError:
                    print("Format tanggal salah. Harap masukkan tanggal dalam format YYYY-MM-DD.")
                    return
                status = input("Masukkan status surat (proses/selesai): ")
                tambah_surat(nomor_surat, pengirim, isi_surat, tanggal_terima, status)
            elif pilihan == 2:
                lihat_surat()
            elif pilihan == 3:
                surat_id = int(input("Masukkan ID surat: "))
                new_nomor_surat = input("Masukkan nomor surat baru: ")
                new_pengirim = input("Masukkan pengirim baru: ")
                new_isi_surat = input("Masukkan isi surat baru: ")
                new_tanggal_terima = input("Masukkan tanggal terima baru (YYYY-MM-DD): ")
                try:
                    new_tanggal_terima = datetime.strptime(new_tanggal_terima, "%Y-%m-%d").date()
                except ValueError:
                    print("Format tanggal salah. Harap masukkan tanggal dalam format YYYY-MM-DD.")
                    return
                new_status = input("Masukkan status surat baru (proses/selesai): ")
                edit_surat(surat_id, new_nomor_surat, new_pengirim, new_isi_surat, new_tanggal_terima, new_status)
            elif pilihan == 4:
                surat_id = int(input("Masukkan ID surat: "))
                hapus_surat(surat_id)
            elif pilihan == 5:
                print("Anda Akan Kembali Ke Menu Admin!!")
                Account.admin_access()
            elif pilihan == 6:
                print("Anda Akan Kembali Ke Menu Login!!")
                Account.main()
            elif pilihan == 7:
                print("Anda Akan Kembali Ke Menu Utama!!")
                menu()
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                halaman_surat()
        except ValueError:
            print("Masukkan angka untuk memilih. Silakan coba lagi.")
            halaman_surat()
    elif role == "user":
        from Auth.account import Account
        from mainmenu import menu
        print("\n--- Halaman Surat ---")
        print("1. Tambah surat baru")
        print("2. Lihat semua surat")
        print("3. Kembali Ke menu user")
        print("4. Kembali ke Menu Login")
        print("5. Kembali ke Menu Utama")
        try:
            pilihan = int(input("Masukkan pilihan: "))
            if pilihan == 1:
                nomor_surat = input("Masukkan nomor surat: ")
                pengirim = input("Masukkan pengirim surat: ")
                isi_surat = input("Masukkan isi surat: ")
                tanggal_terima = input("Masukkan tanggal terima (YYYY-MM-DD): ")
                try:
                    tanggal_terima = datetime.strptime(tanggal_terima, "%Y-%m-%d").date()
                except ValueError:
                    print("Format tanggal salah. Harap masukkan tanggal dalam format YYYY-MM-DD.")
                    return
                status = input("Masukkan status surat (proses/selesai): ")
                tambah_surat(nomor_surat, pengirim, isi_surat, tanggal_terima, status)
            elif pilihan == 2:
                lihat_surat()
            elif pilihan == 3:
                print("Anda Akan Kembali Ke Menu User!!")
                Account.user_access()
            elif pilihan == 6:
                print("Anda Akan Kembali Ke Menu Login!!")
                Account.main()
            elif pilihan == 7:
                print("Anda Akan Kembali Ke Menu Utama!!")
                menu()
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                halaman_surat()
        except ValueError:
            print("Masukkan angka untuk memilih. Silakan coba lagi.")
            halaman_surat()

if __name__ == "__main__":
    buat_tabel()
    halaman_surat()
