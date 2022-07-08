import cryptocode
from package import variables as v

key = v.cryptokey


def encoding(message):
    message = cryptocode.encrypt(message, key)
    return message


def decoding(message):
    str_decoded = cryptocode.decrypt(message, key)
    return message
