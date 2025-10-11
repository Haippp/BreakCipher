import hashBreaker as hb

# pw = '482c811da5d5b4bc6d497ffa98491e38'
# tess = 'md5_raibow_table_rockyou.json'
# hb.useRainbowTable(tess, pw)

path = './wordlist/rockyou.txt'

# hb.hashCrack(pw, file_path)
# hb.useRainbowTable(file_path, pw)

psw = 'b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3'
# path = './wordlist/rockyou.txt'
hb.hashCrack(psw, path)