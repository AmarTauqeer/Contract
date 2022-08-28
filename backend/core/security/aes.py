from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes


def encryption_aes():
    data=b'data to be encrypted'

    data= pad(data,AES.block_size)

    key =get_random_bytes(16)

    with open('aeskey','wb') as f:
        f.write(key)

    cipher = AES.new(key, AES.MODE_CBC)
    e_data = cipher.encrypt(data)

    with open('enc_data','wb') as f:
        f.write(cipher.iv)
        f.write(e_data)

def decryption_aes():
    with open('enc_data','rb') as f:
        iv=f.read(16)
        cipher_data = f.read()

    with open('aeskey','rb') as f:
        key=f.read()

    cipher =AES.new(key, AES.MODE_CBC, iv)

    data = cipher.decrypt(cipher_data)
    data = unpad(data, AES.block_size)

    print(f" decryted data == {data}")

if __name__=='__main__':
    encryption_aes()
    decryption_aes()

