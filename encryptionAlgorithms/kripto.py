import pandas as pd
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode

envanterTablosu = '/home/mrc/PycharmProjects/Network-Programmability/connection/envanterTablosu.xlsx'


# Dış kapsamdaki "sifre" adlı değişkeni tanımla
disKapsamSifre = 'sifre_123'

# Excel dosyasını oku

veri = pd.read_excel(envanterTablosu)


# Şifreleme fonksiyonu
def sifrele(metin, sifre_param):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=b'salt_123',  # Güvenli bir tuz ekleyin
        length=32,
        backend=default_backend()
    )
    anahtar = kdf.derive(sifre_param.encode())
    iv = b'iv_12345678901234'[:16]  # 16 byte uzunluğunda bir IV belirleyin
    cipher = Cipher(algorithms.AES(anahtar), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    sifreli_metin = encryptor.update(metin.encode()) + encryptor.finalize()
    return urlsafe_b64encode(sifreli_metin).decode()


# DEC_PASSWORD sütunundaki metinleri şifrele ve ENC_PASSWORD sütununa yaz
veri['ENC_PASSWORD'] = veri['DEC_PASSWORD'].apply(lambda x: sifrele(str(x), disKapsamSifre))

# Sonuçları Excel dosyasına yaz
veri.to_excel(envanterTablosu, index=False)
