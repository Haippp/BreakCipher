from base64 import b64decode

fFlag = 'd3BqdkpBTXtqaGx6aHlfazNqeTl3YTNrX2g0N2o2azY5fQ=='
try:
    while True:
        fFlag = b64decode(fFlag).decode()
except:
    print('The Flag is:', fFlag)