from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def key_generate():
    key = RSA.generate(2048)

    private_key = key.exportKey()
    publick_key = key.public_key().exportKey()

    with open('public.pem', 'wb') as f:
        f.write(publick_key)

    with open('private.pem', 'wb') as f:
        f.write(private_key)


if __name__ == '__main__':
    key_generate()
