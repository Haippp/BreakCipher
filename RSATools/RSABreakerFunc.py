import sys
from math import gcd
import requests as req
from Crypto.Util.number import long_to_bytes
from gmpy2 import isqrt, iroot

# ============================================= #
#               COMMON FUNCTION                 #
# ============================================= #

def read_encfile(file_path: str) -> dict:
    data = {}

    with open(file_path, 'r') as file:
        for line in file:
            arrData = line.strip().split('=')
            try:
                data[arrData[0].strip()] = int(arrData[1].strip())
            except:
                print('data bukan integer')
                data[arrData[0].strip()] = arrData[1].strip()

    return data

def totient(FactorArr: list) -> int:
    phi = 1
    for f in FactorArr:
        try:
            phi *= int(f[0]) - 1
        except:
            phi *= f - 1
    return phi

def decrypt(ct: int, e: int, n: list, factor: list, /) -> int:
    phi = totient(factor)
    d = pow(e, -1, phi)
    pt = pow(ct, d, n)

    return long_to_bytes(pt)

def continued_fraction(n, d):
    if d == 0:
        return []
    q = n // d
    r = n - q * d
    return [q] + continued_fraction(d, r)

def convergents(n, d):
    hh, kk, h, k = 0, 1, 1, 0
    for x in continued_fraction(n, d):
        hh, kk, h, k = h, k, h * x + hh, k * x + kk
        yield h, k

def modinv(a, m):
    return pow(a, -1, m)

# ============================================= #
#               FUNCTION ATTACK                 #
# ============================================= #

def searchFactorDB(ct: int, e: int,  n: int) -> bytes:
    url = 'https://factordb.com/api?query='

    print('[*] Melakukan pencarian pada https://factordb.com/')
    factorDB = req.get(url + str(n)).json()
    status = factorDB['status']; factor = factorDB['factors']

    match status:
        case 'P':
            print('[!] Status : Nilai n tersebut merupakan prima')
            print('[*] Melanjutkan ke proses Decrypt')
            pt = decrypt(ct, e, n, factor)
        case 'FF':
            print('[!] Status : Semua faktor primanya sudah diketahui')
            print('[*] Melanjutkan ke proses Decrypt')
            pt = decrypt(ct, e, n, factor)
        case 'CF':
            print('[!] Status : Sebagian faktor sudah diketahui, tapi mungkin belum lengkap')
            return
        case _:
            print('[!] Status : Tidak menemukan faktornya')
            return
    
    print(f'[+] Flag Ditemukan! {pt.decode()}\n\n')
    return pt

def lowExp_attack(c, e):
    pt, isRoot = iroot(c, e)
    if isRoot:
        return long_to_bytes(pt)
    return
    

def wienner_attack(c, e, n):
    print('[*] Mencoba menggunakan wienner_attack')
    p, q = 0, 0
    for k, d in convergents(e, n):
        if k != 0:
            phi_n = (e * d - 1) // k
            a, b, c = 1, n - phi_n + 1, n
            delta = pow(b, 2) - 4 * a * c
            if delta >= 0:
                s1 = (-b + isqrt(delta)) // 2 * a
                s2 = (-b - isqrt(delta)) // 2 * a
                if n == s1 * s2:
                    print('[+] P & Q di temukan, anda bisa lanjut keproses selanjutnya')
                    factor = [int(abs(s1)), int(abs(s2))]
                    return factor

    print('[x] Mohon maaf serangan gagal')
    return -1, -1

def common_modulus_attack(c1, c2, e1, e2, N):
    g = gcd(e1, e2)
    if g != 1:
        print("Exponents e1 and e2 must be coprime!", file=sys.stderr)
        sys.exit(1)

    s1 = modinv(e1, e2)
    s2 = (g - e1 * s1) // e2

    temp = modinv(c2, N)
    m1 = pow(c1, s1, N)
    m2 = pow(temp, -s2, N)
    r1 = (m1 * m2) % N

    return long_to_bytes(r1)