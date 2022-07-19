import cryptocode
from package import variables as v

key = v.cryptokey


def encoding(message):
    str_encoded = cryptocode.encrypt(message, key)
    return str_encoded


def decoding(message):
    try:
        str_decoded = cryptocode.decrypt(message, key)
        return str_decoded
    except:
        return False
