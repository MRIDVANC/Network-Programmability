from cryptography.fernet import Fernet

# Anahtarlar ve şifrelerin eşleştirildiği sözlük
KEYS_AND_PASSWORDS = {
    '192.168.1.103': {'anahtar': b'<anahtar1>', 'sifre': 'Turkcell!2023'},
    '192.168.1.104': {'anahtar': b'<anahtar2>', 'sifre': 'Hay2023!'},
    # ... diğer anahtarlar ve şifreler
}


def encrypt_decrypt_password(ip_address, encrypt=True):
    key = Fernet.generate_key()  # Her oturum için yeni bir anahtar oluştur
    cipher_suite = Fernet(key)

    if encrypt:
        # Şifrele
        cipher_text = cipher_suite.encrypt(KEYS_AND_PASSWORDS[ip_address]['sifre'].encode())
        return cipher_text
    else:
        # Şifreyi çöz
        cipher_text = encrypt_decrypt_password(ip_address)  # Şifreleme yapılmış haliyle tekrar çağır
        decrypted_text = cipher_suite.decrypt(cipher_text).decode()
        return decrypted_text


# Şifrelenmiş şifreyi doğrudan döndüren bir fonksiyon
def get_encrypted_password(ip_address):
    return encrypt_decrypt_password(ip_address)


# Anahtarın dışa açık bir şekilde alınmasını sağlayan bir fonksiyon
def get_key(ip_address):
    key = Fernet.generate_key()  # Her oturum için yeni bir anahtar oluştur
    return key
