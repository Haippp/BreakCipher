def hex2str(hex:str, encode="utf-8") -> str:
    """
    mengubah hex menjadi string
    """
    return bytes.fromhex(hex).decode(encoding=encode) 

def hex2bytes(hex:str) ->  bytes:
    """
    mengubah hex menjadi bytes
    """
    return bytes.fromhex(hex)