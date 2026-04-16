# #!/usr/bin/python3
import argparse
import string as s

up = ord('A')
low = ord('a')
alphabet = s.ascii_lowercase
ALPHABET = s.ascii_uppercase

def argparser() -> argparse:
    arg = argparse.ArgumentParser(description="Tools yang berfungsi untuk melakukan seluruh decryption pada enkripsi alphabetic")
    arg.add_argument('-c', '--ciphertext', type=str, help='Encrypted Message/Ciphertext', required=True)
    arg.add_argument('-p', '--pola', type=str ,help='Pola dari sebuah flag')
    arg.add_argument('-e', '--enc-type', type= int, help="""
    Memilih enkripsi apa yang akan digunakan
    1 : ROT Cipher
    2 : Atbash
    3 : A1Z26
    Jika tidak memilih salah satunya maka akan secara otomatis menggunakan semua
""")

    return arg

def bf_rot(text: str, pola_flag = None) -> str:
    print('[*] Melakukan bruteforce enkripsi rot')
    for i in range(1, 27):
        dec = ''
        for c in text:
            if c.isupper():
                dec += chr((ord(c) - up + i) % 26 + up)
            elif c.islower():
                dec += chr((ord(c) - low + i) % 26 + low)
            else:
                dec += c
        if pola_flag != None:
            print('[+] Pola di temukan')
            if pola_flag in dec:
                print(f'[+] Flagnya adalah : {dec}')
                return
        else :
            print(f'[{i}] result :', dec)

def atbash(text: str) -> str:
    dec = ''
    for c in text:
        if c.islower():
            dec += ALPHABET[::-1][ALPHABET.index('A')]
        elif c.isupper():
            dec += ALPHABET[::-1][ALPHABET.index('A')]
        else:
            dec += c
    print(f'[+] result :', dec)
    return dec

if __name__ == "__main__":
    args = argparser()
    arg = args.parse_args()

    ct = arg.ciphertext

    pola = arg.pola if arg.pola else None
    enc_type = arg.enc_type if arg.enc_type else 0

    match enc_type:
        case 0:
            bf_rot(ct, pola)
            atbash(ct)
        case 1:
            bf_rot(ct, pola)
        case 2:
            atbash(ct)
        case _:
            print("\n[!] Pilihan salah. Berikut panduan untuk --enc-type:")
            msg = next(a.help for a in args._actions if a.dest == "enc_type")
            print(msg)