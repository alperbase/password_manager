import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def crypt(password, direction, message="", hashed=b"", salt_=b""):
    password = password.encode()
    message = message.encode()
    if salt_ == b"":
        salt_ = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    if direction == "en":
        donder = (f.encrypt(message), salt_)
    elif direction == "de":
        donder = f.decrypt(hashed)
    else:
        donder = ""
    return donder