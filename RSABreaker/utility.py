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