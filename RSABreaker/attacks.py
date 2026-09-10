import sys
from math import gcd
import requests as req
from Crypto.Util.number import long_to_bytes
from gmpy2 import mpz, isqrt, iroot
from string import printable
import time as t

def isPrintable(text:str) -> bool:
    if all(t in printable for t in text):
        return True
    else:
        return False


class RSAAttacks:
    def __init__(self, c:int, n:int, e = 65537, max_time = 0):
        self.c = c
        self.e = e
        self.n = n
        self.factor = []
        self.max_time = max_time
        self.start = t.time()

    def isMaxTime(self):
        if t.time() - self.start > self.max_time:
            return True
        return False

    def isHaveFactor(self) -> bool:
        if len(self.factor) == 0:
            print("[!] cari factor terlebih dahulu")
            return False
        else: 
            return True

    def totient(self) -> int:
        phi = 1
        for f in self.factor:
            try:
                phi *= int(f[0]) - 1
            except:
                phi *= f - 1
        return phi

    def decrypt(self) -> bytes:
        phi = self.totient()
        d = pow(self.e, -1, phi)
        print(d)
        pt = long_to_bytes(pow(self.c, d, self.n))

        try:
            if isPrintable(flag := pt.decode()):
                print('[+] ciphertext berhasil di decrypt :', flag)
        except:
            print(pt)
        
        return 
    
    def searchFactorDB(self) -> bytes:
        url = 'https://factordb.com/api?query='

        print('[*] Melakukan pencarian pada https://factordb.com/')
        factorDB = req.get(url + str(self.n)).json()
        status = factorDB['status']; self.factor = factorDB['factors']

        match status:
            case 'P':
                print('[!] Status : Nilai n tersebut merupakan prima')
                print('[*] Melanjutkan ke proses Decrypt')
                pt = self.decrypt()
            case 'FF':
                print('[!] Status : Semua faktor primanya sudah diketahui')
                print('[*] Melanjutkan ke proses Decrypt')
                pt = self.decrypt()
            case 'CF':
                print('[!] Status : Sebagian faktor sudah diketahui, tapi mungkin belum lengkap')
                return
            case _:
                print('[!] Status : Tidak menemukan faktornya')
                return

        # try:
        #     print(f'[+] Flag Ditemukan! {pt.decode()}\n\n')
        # except:
        #     print(b'[+] Flag Ditemukan!: ' + pt)
        
        return pt
    
    def fermat_factor(self) -> list:
        print('[*] Melakukan pencarian factor menggunakan teori fermat factor')
        a = isqrt(self.n)
        if a * a < self.n:
            a += 1

        while True:

            if self.isMaxTime():
                print('[!] pencarian factor berhenti karena mencapai batas waktu')
                return
        
            b2 = a * a - self.n
            b = isqrt(b2)

            if b * b == b2:
                print('[+] P & Q di temukan, anda bisa lanjut keproses selanjutnya')
                self.factor = [a - b, a + b]
                return self.factor
            
            a += 1

    def lowExp_attack(self):
        pt, isRoot = iroot(self.c, self.e)
        if isRoot:
            return long_to_bytes(pt)
        return
    
    def continued_fraction(self, n, d) -> int:
        if d == 0:
            return []
        q = n // d
        r = n - q * d
        return [q] + self.continued_fraction(d, r)

    def convergents(self, n, d):
        hh, kk, h, k = 0, 1, 1, 0
        for x in self.continued_fraction(n, d):
            hh, kk, h, k = h, k, h * x + hh, k * x + kk
            yield h, k

    def wienner_attack(self):
        print('[*] Mencoba menggunakan wienner_attack')
        p, q = 0, 0
        for k, d in self.convergents(self.e, self.n):
            if k != 0:
                phi_n = (self.e * d - 1) // k
                a, b, c = 1, self.n - phi_n + 1, self.n
                delta = pow(b, 2) - 4 * a * c
                if delta >= 0:
                    s1 = (-b + isqrt(delta)) // 2 * a
                    s2 = (-b - isqrt(delta)) // 2 * a
                    if self.n == s1 * s2:
                        print('[+] P & Q di temukan, anda bisa lanjut keproses selanjutnya')
                        self.factor = [int(abs(s1)), int(abs(s2))]
                        return self.factor

        print('[x] Mohon maaf serangan gagal')
        return -1, -1