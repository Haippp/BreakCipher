import sys
import hashlib
import json

result_file = 'raibow_table.json'

def creatRainbowTable(file:str, alg: int) -> json:
    print('[*] Membuat rainbow table dalam bentuk json')
    data = {}
    
    print('[*] Melakukan hashing pada wordlist')
    with open(file, 'r', encoding='latin-1') as file:
        try:
            for pswd in file:
                pswd = pswd.strip()
                line = pswd.encode()
                match alg:
                    case 32:
                        line = hashlib.md5(line)
                    case 40:
                        line = hashlib.sha1(line)
                    case 64:
                        line = hashlib.sha256(line)
                    case 128:
                        line = hashlib.sha512(line)
                    case _:
                        return
                data[line.digest().hex()] = pswd
        except:
            print('[x] Terjadi error ketika proses sedang berlangsung')
            print(pswd)

    print('[*] Menggabungkan semua data kedalam file json')
    with open(result_file, 'w') as file:
        json.dump(data, file, indent=4)
    print('[+] Pembuatan rainbow table selesai! silahkan cek pada file', result_file)

def hashCheck(hexText: str) ->  int:
    print('[*] Melakukan pengecekan algorimat hash yang digunakan')
    lh = len(hexText)
    match lh:
        case 32:
            print('[!] Hash yang digunakan adalah MD5')
            return 32
        case 40:
            print('[!] Hash yang digunakan adalah SHA-1')
            return 40
        case 64:
            print('[!] Hash yang digunakan adalah SHA-256')
            return 64
        case 128:
            print('[!] Hash yang digunakan adalah SHA-512')
            return 128
        case _:
            print('[x] Algoritma hash yang digunakan tidak diketahui')
            return 0


def hashCrack(hexText: str, wordlist_path: str) -> str:
    print('[*] Melakukan prosses cracking hash:', hexText)
    alg = hashCheck(hexText)
    creatRainbowTable(wordlist_path, alg)
    with open(result_file, 'r') as file:
        rainbow_table = json.load(file)
    
    try:
        pswd = rainbow_table[hash]
        print('[+] Hash ada dalam table tersebut, result :', pswd)
        return pswd
    except:
        print('[x] Mohon maaf tidak ada hash yang sama pada data')
        return

def useRainbowTable(table_file_path: json, hash: str) -> str:
    print('[*] Menggunakan rainbow table yang sudah ada')
    with open(table_file_path, 'r') as file:
        rainbow_table = json.load(file)
    
    try:
        pswd = rainbow_table[hash]
        print('[+] Hash ada dalam table tersebut, result :', pswd)
        return pswd
    except:
        print('[x] Mohon maaf tidak ada hash yang sama pada data')
        return