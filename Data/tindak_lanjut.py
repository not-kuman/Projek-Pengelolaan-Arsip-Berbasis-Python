import sqlite3
def tindak_lanjut():
    conn =  sqlite3.connect('DB_Arsip.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NO EXISTS tindak lanjut (
                   tindak_lanjut_id INTEGER PRIMARY KEY,
                   surat_id INTEGER FOREIGN KEY(REFRENCES surat),
                   tindakan TEXT,
                   tanggal_tindak DATE)''')
    
    tindak_lanjut_id = int(input("Masukan tindak lanjut id: "))
    surat_id = int(input("Masukan surat id: "))
    tindakan = input("Masukan tindakan: ")
    tanggal_tindak = int(input("Masukan tanggal tindak: "))

    cursor.execute("INSERT INTO tindak lanjut (tindak_lanjut_id, surat_id, tindakan, tanggal_tindak) VALUE (?, ?, ?, ?)",(tindak_lanjut_id, surat_id, tindakan, tanggal_tindak))
    
    conn.commit()
    conn.close()
