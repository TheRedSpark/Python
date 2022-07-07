import rsa
import mysql.connector
from package import variables as v

ort = "home"
database = "Selma"


def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(512)
    with open('keys/publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))


def loadKeys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey


def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False


def sign(message, key):
    return rsa.sign(message.encode('ascii'), key, 'SHA-1')


def verify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key, ) == 'SHA-1'
    except:
        return False


#generateKeys()
privateKey, publicKey = loadKeys()
#message = input('Write your message here:')
message = "gasfsdfwerrfasdaserfdasdsadsdwe"
print(len(message))
ciphertext = encrypt(message, publicKey)
signature = sign(message, privateKey)
text = decrypt(ciphertext, privateKey)
print(f'Cipher text: {ciphertext}')
print(len(ciphertext))
print(type(ciphertext))
print(len(str(ciphertext)))
print(f'Signature: {signature}')
print(len(signature))
if text:
    print(f'Message text: {text}')
else:
    print(f'Unable to decrypt the message.')

if verify(text, signature, publicKey):
    print("Successfully verified signature")
else:
    print('The message signature could not be verified')

bla

mydb = mysql.connector.connect(
    host=v.host(ort),
    user=v.user(ort),
    passwd=v.passwd(ort),
    database=v.database(database),
    auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()
my_cursor.execute(f"UPDATE `Test`.`Cipher` SET `Pass` = {message} WHERE (`idCipher` = 4);")
mydb.commit()
my_cursor.close()