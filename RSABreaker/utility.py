from Crypto.Util.number import long_to_bytes

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