import subprocess
import zipfile
import os
import threading
from colorama import init, Fore, Style
from time import sleep as turu
import sys as memek

def install_module(namamodul): # buat nginstallin modul otomatis
    subprocess.check_call([memek.executable, "-m", "pip", "install", namamodul])

try:
    from colorama import init, Fore, Style
except ImportError:
    install_module('colorama')
    from colorama import init, Fore, Style

init()

zip_file_path = None
password_list_path = None
stop_flag = threading.Event()
cracking_thread = None
banner = """
{0}
 ___     ___                                   ___     ___ 
|  _|___|_  |_____ _     _____             _  |  _|___|_  |
| | |   | | |__   |_|___|     |___ ___ ___| |_| | |   | | |
| | | | | | |   __| | . |   --|  _| .'|  _| '_| | | | | | | - adjidev 2024
| |_|___|_| |_____|_|  _|_____|_| |__,|___|_,_| |_|___|_| |
|___|   |___|       |_|                       |___|   |___|

ketik help atau ? jika Anda tidak tahu cara menggunakannya
{1}
""".format(Fore.CYAN, Style.RESET_ALL)

def ngetik(teks): # animasi ngetik
    for i in teks:
        memek.stdout.write(i)
        memek.stdout.flush()
        turu(0.01)

def buat_file(nama_file): # buat file .txt nya
    try:
        with open(nama_file, 'w') as file:
            file.write("Ini adalah file sementara.\n")
        ngetik(Fore.GREEN + f"File {nama_file} dibuat.\n" + Style.RESET_ALL)
    except Exception as e:
        ngetik(Fore.RED + f"Terjadi kesalahan saat membuat file: {e}\n" + Style.RESET_ALL)

def set_password_file(nama_file, passwords): # setpwnya
    try:
        with open(nama_file, 'w') as file:
            for password in passwords:
                file.write(password + "\n")
        ngetik(Fore.GREEN + f"File password {nama_file} dibuat dengan password: {', '.join(passwords)}.\n" + Style.RESET_ALL)
        global password_list_path
        password_list_path = nama_file
    except Exception as e:
        ngetik(Fore.RED + f"Terjadi kesalahan saat membuat file password: {e}\n" + Style.RESET_ALL)

def mulai_cracking(): # mulai crack
    global cracking_thread, stop_flag
    if zip_file_path and password_list_path:
        stop_flag.clear()
        ngetik(Fore.YELLOW + f"Memulai brute force dengan daftar password {password_list_path} pada file ZIP {zip_file_path}..." + Style.RESET_ALL)
        cracking_thread = threading.Thread(target=crack_password, args=(password_list_path, zip_file_path))
        cracking_thread.start()
    else:
        ngetik(Fore.RED + "Harap berikan file ZIP dan file daftar password sebelum memulai proses cracking.\n" + Style.RESET_ALL)

def berhenti_cracking(): # buat stopnya
    global stop_flag
    stop_flag.set()
    ngetik(Fore.YELLOW + "Menghentikan proses cracking...\n" + Style.RESET_ALL)

def terima_file_zip(file_path): # sama kayak yang dibawah
    global zip_file_path
    try:
        zip_file_path = os.path.join('.', os.path.basename(file_path))
        with open(file_path, 'rb') as source_file:
            with open(zip_file_path, 'wb') as dest_file:
                dest_file.write(source_file.read())
        ngetik(Fore.GREEN + "File ZIP diterima. Sekarang berikan file daftar password.\n" + Style.RESET_ALL)
    except Exception as e:
        ngetik(Fore.RED + f"Terjadi kesalahan saat menerima file ZIP: {e}\n" + Style.RESET_ALL)

def terima_file_daftar_password(file_path): # buat nerima file password
    global password_list_path
    try:
        password_list_path = os.path.join('.', os.path.basename(file_path))
        with open(file_path, 'rb') as source_file:
            with open(password_list_path, 'wb') as dest_file:
                dest_file.write(source_file.read())
        ngetik(Fore.GREEN + f"Daftar password {password_list_path} diterima.\n" + Style.RESET_ALL)
    except Exception as e:
        ngetik(Fore.RED + f"Terjadi kesalahan saat menerima file daftar password: {e}\n" + Style.RESET_ALL)

def crack_password(password_list, zip_file): # ini buat ngecrack sandi kominfo s
    idx = 0
    try:
        with open(password_list, 'r') as file:
            for line in file:
                if stop_flag.is_set():
                    ngetik(Fore.YELLOW + "Proses cracking dihentikan.\n" + Style.RESET_ALL)
                    bersihkan_file_sementara()
                    return
                for word in line.split():
                    idx += 1
                    ngetik(Fore.CYAN + f"Upaya {idx}" + Style.RESET_ALL)
                    try:
                        with zipfile.ZipFile(zip_file, 'r') as zf:
                            zf.extractall(pwd=word.encode())
                        password = word
                        ngetik(Fore.GREEN + f"Password ditemukan: {password}\n" + Style.RESET_ALL)
                        bersihkan_file_sementara()
                        return
                    except RuntimeError as e:
                        if "Bad password" in str(e):
                            ngetik(Fore.RED + f"Upaya {idx}: Gagal - Password salah\n" + Style.RESET_ALL)
                            continue
                    except Exception as e:
                        ngetik(Fore.RED + f"Upaya {idx}: Terjadi kesalahan - {e}\n" + Style.RESET_ALL)
                        continue
    except FileNotFoundError as e:
        ngetik(Fore.RED + f"File daftar password tidak ditemukan: {e}\n" + Style.RESET_ALL)
    except Exception as e:
        ngetik(Fore.RED + f"Terjadi kesalahan yang tidak terduga: {e}\n" + Style.RESET_ALL)

    ngetik(Fore.RED + "Password tidak ditemukan dalam daftar.\n" + Style.RESET_ALL)
    bersihkan_file_sementara()

def bersihkan_file_sementara(): # ini fungsinya buat bersihin file biar gak penuh memo kalian
    global zip_file_path, password_list_path
    try:
        if zip_file_path and os.path.exists(zip_file_path):
            os.remove(zip_file_path)
            ngetik(Fore.GREEN + f"{zip_file_path} dihapus" + Style.RESET_ALL)
        if password_list_path and os.path.exists(password_list_path):
            os.remove(password_list_path)
            ngetik(Fore.GREEN + f"{password_list_path} dihapus" + Style.RESET_ALL)
    except Exception as e:
        ngetik(Fore.RED + f"Terjadi kesalahan saat menghapus file sementara: {e}\n" + Style.RESET_ALL)

def main():
    global zip_file_path, password_list_path

    ngetik(banner)

    while True:
        command = input("> ").strip().lower()

        if command.startswith("c "):
            nama_file = command.split()[1]
            buat_file(nama_file)
        elif command.startswith("setpw "):
            parts = command.split()
            nama_file = parts[1]
            passwords = parts[2:]
            set_password_file(nama_file, passwords)
        elif command == "crack":
            mulai_cracking()
        elif command == "stop":
            berhenti_cracking()
        elif command.startswith("zip "):
            file_path = command.split()[1]
            terima_file_zip(file_path)
        elif command.startswith("uploadpasswordlist "):
            file_path = command.split()[1]
            terima_file_daftar_password(file_path)
        elif command.startswith("help"):
            ngetik(f"{Fore.GREEN}Contoh:\npertama buat file.txt dengan mengetik ( create passwordlist.txt )\nkedua tambahkan password pada passwordlist.txt atau dengan mengetik ( setpassword passwordlist.txt password1 password2 admin1 admin2 admin3 admin4 admin5 )\ndan akhirnya mulai cracking dengan mengetik ( crack )\n")
        elif command == "exit":
            ngetik(Fore.YELLOW + "Keluar..." + Style.RESET_ALL)
            break
        else:
            ngetik(Fore.RED + "Perintah tidak dikenal. Perintah yang tersedia: create <filename>, setpassword <filename> password1 password2 ..., crack, stop, uploadzip <file_path>, uploadpasswordlist <file_path>, exit.\n" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
