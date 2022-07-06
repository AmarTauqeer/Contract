import base64
import os

from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

############## global variables ##########################################

BLOCK_SIZE = 16
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


############## global variables ##########################################


class RsaAesDecrypt():

    def rsa_aes_decrypt(self, data):
        list_data = list(data.items())
        cwd = os.getcwd()
        # reading encrypted aes keys
        with open(cwd + '/core/security/bundle' + list_data[0][1] + '.enc', 'rb') as f:
            e_aes_key = f.read(256)
            f.close()

        # reading private key
        with open(cwd + '/core/security/private.pem') as f:
            key = f.read()
            f.close()

        # rsa cipher with private key
        private_key = RSA.importKey(key)
        rsa_cipher = PKCS1_OAEP.new(private_key)
        aes_key = rsa_cipher.decrypt(e_aes_key)
        # handling data without ids
        if 'type_id' in data.keys():
            del data['type_id']
        elif 'contractor_id' in data.keys():
            del data['contractor_id']
        elif 'contract_id' in data.keys():
            del data['contract_id']
        elif 'obligation_id' in data.keys():
            del data['obligation_id']
        elif 'signature_id' in data.keys():
            del data['signature_id']

        ciphers = []
        for key in data:
            key_value = bytes(data[key], 'utf-8')
            key_value = base64.b64decode(key_value)
            # handling nonce/ block sizing
            iv = key_value[:16]
            aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            # decryption
            decrypted_data = unpad(aes_cipher.decrypt(key_value[16:])).decode('utf-8')
            cipher_data = {
                key: decrypted_data
            }
            ciphers.append(cipher_data)
        return ciphers

# if __name__ == '__main__':
#     obj = RsaAesDecrypt()
#     a=obj.rsa_aes_decrypt()
