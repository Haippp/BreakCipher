import argparse

parser = argparse.ArgumentParser(description="""
    Usage: Alphabetic CIPHERTEXT POLA_FLAG()
    melakukan bruteforce enkripsi caesar cipher

    option:
    -p      : untuk menambahkan pola flag, dan menampilkan flagnya jika ada
    """)

parser.add_argument('-c')
parser.add_argument('-p')