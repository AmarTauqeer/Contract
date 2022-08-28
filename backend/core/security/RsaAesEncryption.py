import base64
import os
import re

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto import Random

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

##############global variables##########################################

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


############# end global variables

class RsaAesEncrypt():

    def rsa_aes_encrypt(self, data):
        # generate random aes keys
        aes_key = get_random_bytes(16)
        # get current directory and read public key
        cwd = os.getcwd()
        with open(cwd + '/core/security/public.pem', 'rb') as f:
            pub_key = f.read()
            f.close()

        # import rsa public key and make rsa cipher
        rsa_key = RSA.importKey(pub_key)
        rsa_cipher = PKCS1_OAEP.new(rsa_key)
        # encrypted aes keys with rsa
        e_aes_key = rsa_cipher.encrypt(aes_key)

        # data items in list
        list_data = list(data.items())

        ciphers = []
        for key in data:
            key_value = data[key]
            # add pad
            key_value = pad(key_value)
            # conversion into bytes
            key_value = key_value.encode('utf-8')
            # handle nonce (16 block size problem)
            iv = Random.new().read(AES.block_size)
            aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            # encryption with aes cipher
            e_data = iv + aes_cipher.encrypt(key_value)
            # conversion into b64
            e_data = base64.b64encode(e_data)
            # collection of ciphers
            cipher_data = {
                key: self.escape_special_character(e_data)
            }
            ciphers.append(cipher_data)
        # store encrypted aes key separately
        with open(cwd + '/core/security/bundle' + list_data[0][1] + '.enc', 'wb') as f:
            f.write(e_aes_key)
            f.close()
        return ciphers

    def escape_special_character(self, data):
        pattern_regex = r"[ -\/:-@\[-\`{-~]"
        return re.sub(r'([\'\"\\\.\\\\*\?\[\^\]\$\(\)\{\}\!\<\>\|\:\-])', r'\\\1', str(data.decode("utf-8")))

# test locally
# if __name__ == '__main__':
#     message = b'amendment description'
#     obj =RsaAesEncrypt()
#     a=obj.rsa_aes_encrypt(message)
#     # print(a)
