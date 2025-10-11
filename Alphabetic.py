# #!/usr/bin/python3
import sys

up = ord('A')
low = ord('a')

def bf_rot(text: str, pola_flag = None) -> str:
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
            if pola_flag in dec:
                print(f'flag is : {dec}')
                return
        else :
            print(f'[{i}] result :', dec)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
        Usage: Alphabetic CIPHERTEXT POLA_FLAG(OPSIONAL)
        """)
        exit()

    print(sys.argv)
    ct = sys.argv[2]
    pola = sys.argv[3]
    bf_rot(ct, pola)