from RSABreakerFunc import *
import argparse

def args_parser():
    parser = argparse.ArgumentParser(description='RSA Breaker Tool - Menganalisis dan mengeksploitasi kerentanan RSA')

    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="Path file hasil enkripsi"
    )

    parser.add_argument(
        "-t", "--type",
        type=str,
        default='all',
        choices=["lowExp", "wiener", "common_modulus"],
        help="Jenis kerentanan/attack yang digunakan"
    )
    
    return parser.parse_args()

def main():
    args = args_parser()
    pub_key = read_encfile(args.file)

    match args.type:
        case 'wiener':
            factor = wienner_attack(pub_key['c'], pub_key['e'], pub_key['n'])
            flag = decrypt(pub_key['c'], pub_key['e'], pub_key['n'], factor)
            print(flag)
        case 'lowExp':
            lowExp_attack(pub_key['c'], pub_key['e'])
        case 'all':
            searchFactorDB(pub_key['c'], pub_key['e'], pub_key['n'])
        case _:
            print('Tipe tidak diketahui silahkan pilih salah satu dari yang dibawah ini')
            print('''

''')
        

if __name__ == '__main__':
    main()