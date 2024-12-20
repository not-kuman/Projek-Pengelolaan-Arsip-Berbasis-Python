import sqlite3
role = None

def tindak_lanjut():
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
    try:
        tindak_lanjut_id = int(input("Masukkan tindak lanjut ID: "))
        surat_id = int(input("Masukkan surat ID: "))
        tindakan = input("Masukkan tindakan: ")
        tanggal_tindak = input("Masukkan tanggal tindak (format YYYY-MM-DD): ")
        import datetime
        try:
            datetime.datetime.strptime(tanggal_tindak, '%Y-%m-%d')
        except ValueError:
            print("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
            return
        cursor.execute(
            "INSERT INTO tindak_lanjut (tindak_lanjut_id, surat_id, tindakan, tanggal_tindak) VALUES (?, ?, ?, ?)",
            (tindak_lanjut_id, surat_id, tindakan, tanggal_tindak)
        )
        conn.commit()
        print("Data tindak lanjut berhasil disimpan!")
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan pada database: {e}")

    except ValueError:
        print("Input tidak valid. Pastikan data sesuai dengan tipe yang diminta.")
    
    finally:
        conn.close()
def main_menu():
    from Auth.account import Account
    from mainmenu import menu
    while True:
        print("\n=== Halaman Utama ===")
        print("1. Login")
        print("2. Keluar")
        choice = input("Pilih opsi (1/2): ")
        if choice == "1":
            role = Account
            if role == "admin":
                Account.admin_access()
            elif role == "user":
                print("Anda tidak memiliki akses ke halaman admin.")
        elif choice == "2":
            print("Keluar dari menu. Kembali Ke Menu Awal!")
            menu()
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
