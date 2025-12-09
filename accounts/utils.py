import os

from cryptography.fernet import Fernet


os_fernet_key = os.getenv('FERNET_KEY')
fernet_key = os_fernet_key.encode() if os_fernet_key else b'Poxa :('
cipher_suite = Fernet(fernet_key)
