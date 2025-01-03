def menu():
    try:
        from Auth.account import Account
        while True:
            print("\nMenu Utama:")
            print("1. Mulai")
            print("2. Keluar")
            choice = input("Pilih opsi (1, 2): ")
            
            if choice == "1":
                Account.main()
            elif choice == "2":
                print("Terima kasih telah menggunakan aplikasi.")
                break
            else:
                print("Opsi tidak valid. Harap pilih 1 atau 2.")
    except ModuleNotFoundError:
        print("File 'Auth/account.py' tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    menu()