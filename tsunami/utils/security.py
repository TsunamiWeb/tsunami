import os
import hashlib
import base64


def gen_salt(size=16):
    return os.urandom(size).hex()


def gen_password(password, iterations=24000):
    _salt = gen_salt()
    return base64.b64encode(
        hashlib.pbkdf2_hmac('sha256',
                            password.encode('utf-8'),
                            _salt.encode('utf-8'),
                            iterations)).decode(), _salt


def get_password(password, salt, iterations=24000):
    return base64.b64encode(
        hashlib.pbkdf2_hmac('sha256',
                            password.encode('utf-8'),
                            salt.encode('utf-8'),
                            iterations)).decode()
