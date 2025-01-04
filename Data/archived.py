import sqlite3
Data = []
Data.append("DB_Arsip.db")
def tambah_arsip():
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS archives (
                       archives_id INTEGER PRIMARY KEY,
                       title TEXT,
                       description TEXT,
                       file_path TEXT,
                       category_id INTEGER,
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    print("Tabel Arsip berhasil dibuat!")
    
    try:
        archives_id = int(input("Masukkan Archives ID: "))
        title = input("Masukkan Title: ")
        description = input("Masukkan Description: ")
        file_path = input("Masukkan File Path: ")
        category_id = int(input("Masukkan Category ID: "))
        
        cursor.execute("INSERT INTO archives (archives_id, title, description, file_path, category_id) VALUES (?, ?, ?, ?, ?)", 
                       (archives_id, title, description, file_path, category_id))
        conn.commit()
        print("Data arsip berhasil ditambahkan!")
    except ValueError:
        print("Input tidak valid. Pastikan Archives ID dan Category ID berupa angka.")
    finally:
        conn.close()
    halaman_arsip()

def lihat_arsip():
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM archives")
    rows = cursor.fetchall()
    
    if rows:
        print("Data Arsip:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Description: {row[2]}, File Path: {row[3]}, Category ID: {row[4]}")
    else:
        print("Tidak ada data arsip.")
    
    conn.close()
    halaman_arsip()

def edit_arsip():
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM archives")
    rows = cursor.fetchall()
    
    if rows:
        print("Data Arsip Sebelum Pembaruan:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Description: {row[2]}, File Path: {row[3]}, Category ID: {row[4]}")
        
        try:
            archives_id = int(input("Masukkan ID arsip yang ingin diubah: "))
            cursor.execute("SELECT * FROM archives WHERE archives_id = ?", (archives_id,))
            if cursor.fetchone():
                title = input("Masukkan Title Baru: ")
                description = input("Masukkan Description Baru: ")
                file_path = input("Masukkan File Path Baru: ")
                category_id = int(input("Masukkan Category ID Baru: "))
                
                cursor.execute("UPDATE archives SET title = ?, description = ?, file_path = ?, category_id = ?, updated_at = CURRENT_TIMESTAMP WHERE archives_id = ?", 
                               (title, description, file_path, category_id, archives_id))
                conn.commit()
                print("Data arsip berhasil diperbarui!")
            else:
                print("ID arsip tidak ditemukan.")
        except ValueError:
            print("Input tidak valid. Pastikan Archives ID dan Category ID berupa angka.")
    else:
        print("Tidak ada data untuk diperbarui.")
    
    conn.close()
    halaman_arsip()

def hapus_arsip():
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM archives")
    rows = cursor.fetchall()
    
    if rows:
        print("Data Arsip Sebelum Penghapusan:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Description: {row[2]}, File Path: {row[3]}, Category ID: {row[4]}")
        
        try:
            archives_id = int(input("Masukkan ID arsip yang ingin dihapus: "))
            cursor.execute("SELECT * FROM archives WHERE archives_id = ?", (archives_id,))
            if cursor.fetchone():
                cursor.execute("DELETE FROM archives WHERE archives_id = ?", (archives_id,))
                conn.commit()
                print("Data arsip berhasil dihapus!")
            else:
                print("ID arsip tidak ditemukan.")
        except ValueError:
            print("Input tidak valid. Pastikan Archives ID berupa angka.")
    else:
        print("Tidak ada data untuk dihapus.")
    
    conn.close()
    halaman_arsip()

def tampilkan_arsip():
    conn = sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM archives")
    rows = cursor.fetchall()
    
    if rows:
        print("Data Arsip:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Description: {row[2]}, File Path: {row[3]}, Category ID: {row[4]}")
    else:
        print("Tidak ada data arsip.")
    
    conn.close()
    halaman_arsip()

def halaman_arsip():
    from Auth.account import Account
    account = Account()  # Create an instance of Account
    role = account.get_role()  # Call get_role without arguments
    print(f"Role yang didapat: {role}")   
    if role == 'admin':
        while True:
            from Auth.account import Account
            from menu import menu
            print("\n--- Halaman Arsip ---")
            print("1. Tambah data arsip")
            print("2. Lihat data arsip")
            print("3. Edit data arsip")
            print("4. Hapus data arsip")
            print("5. Tampilkan data arsip")
            print("6. Kembali ke Menu admin")
            print("7. Kembali ke Menu Login")
            print("8. Kembali ke Menu Utama")
            try:
                pilihan = int(input("Masukkan pilihan: "))
                if pilihan == 1:
                    tambah_arsip()
                elif pilihan == 2:
                    lihat_arsip()
                elif pilihan == 3:
                    edit_arsip()
                elif pilihan == 4:
                    hapus_arsip()
                elif pilihan == 5:
                    tampilkan_arsip()
                elif pilihan == 6:
                    print("Anda Akan Kembali Ke Menu admin!!")
                    Account.admin_access()
                elif pilihan == 7:
                    print("Anda Akan Kembali Ke Menu Login!!")
                    Account.main()
                elif pilihan == 8:
                    print("Anda Akan Kembali Ke Menu Utama!!")
                    menu()
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
                    halaman_arsip()
            except ValueError:
                print("Masukkan angka untuk memilih. Silakan coba lagi.")
                halaman_arsip()
    elif role == 'user' :
        while True:
            from Auth.account import Account
            from menu import menu
            print("\n--- Halaman Arsip User ---")
            print("1. Tambah data arsip")
            print("2. Lihat data arsip")
            print("3. Kembali ke Menu User")
            print("4. Kembali ke Menu Login")
            print("5. Kembali ke Menu Utama")
            try:
                pilihan = int(input("Masukkan pilihan: "))
                if pilihan == 1:
                    tambah_arsip()
                elif pilihan == 2:
                    lihat_arsip()
                elif pilihan == 3:
                    print("Anda Akan Kembali Ke Menu admin!!")
                    Account.user_access()
                elif pilihan == 4:
                    print("Anda Akan Kembali Ke Menu Login!!")
                    Account.main()
                elif pilihan == 5:
                    print("Anda Akan Kembali Ke Menu Utama!!")
                    menu()
                else:
                    print("Pilihan tidak valid.")
                    halaman_arsip()
            except ValueError:
                print("Masukkan angka untuk memilih.")  
    else:
        print("Role tidak valid. Silahkan coba lagi")
        return
if __name__ == "__main__":
    halaman_arsip()