import pandas as pd
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64decode
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException

# Dış kapsamdaki "sifre" adlı değişkeni tanımla
disKapsamSifre = 'sifre_123'

# Excel dosyasını oku
dosyaAdi = 'envanterTablosu.xlsx'
veri = pd.read_excel(dosyaAdi)


# Şifre çözme fonksiyonu
def sifre_coz(sifreli_metin, sifre_param):
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
    decryptor = cipher.decryptor()
    sifreli_metin = urlsafe_b64decode(sifreli_metin)
    metin = decryptor.update(sifreli_metin) + decryptor.finalize()
    return metin.decode()


# ENC_PASSWORD sütunundaki şifreli metinleri çözerek DEC_PASSWORD sütununu güncelle
veri['DEC_PASSWORD'] = veri['ENC_PASSWORD'].apply(lambda x: sifre_coz(x, disKapsamSifre))

# Cihazlara bağlanma ve işlemleri gerçekleştirme
for index, row in veri.iterrows():
    switch_device = {
        'device_type': row['DEVICE TYPE'],
        'ip': row['IP ADDRESS'],
        'username': row['USERNAME'],
        'password': row['DEC_PASSWORD'],
        'port': 22,
    }

    try:
        # Switch'e bağlan
        net_connect = ConnectHandler(**switch_device)
        print(f"Bağlantı başarılı. {row['SWITCHNAME']} switch'ine bağlandınız.")
        """
        # "show interfaces" komutunu gönder ve sonucunu al
        output = net_connect.send_command('show interfaces')
        print("show interfaces komutunun sonucu:\n")
        print(output)

        # Diğer işlemler devam ediyor
        # Örnek 1: "show interfaces" komutunu gönder ve sonucunu al
        output = net_connect.send_command('show interface status')
        print("show interface status komutunun sonucu:\n")
        print(output)
        
        
        output3 = net_connect.send_command('show mac address-table')
        print("\nshow mac address komutunun sonucu:\n")
        print(output3)
         

        
        # Örnek 3: Cihazın konfigürasyonunu değiştirme
        config_commands = [
            'conf t',
            'interface ethernet 1/1',
            'description configDeneme',
            'no shutdown'
        ]
        output4 = net_connect.send_config_set(config_commands)
        print("\nKonfigürasyon değişikliği sonucu:\n")
        output5 = net_connect.send_command('show run interface ethernet 1/1')
        print(output4)
        print(output5)

        # Yedekleme komutunu gönder
        output = net_connect.send_command('write memory')
        print("Yedekleme komutunun sonucu:\n")
        print(output)
        """
        # Örnek 2: "show lldp" komutunu gönder ve sonucunu al
        output2 = net_connect.send_command('show lldp neighbors')
        print("\nshow lldp komutunun sonucu:\n")
        print(output2)

        # Bağlantıyı kapat
        net_connect.disconnect()

    except NetMikoTimeoutException:
        print(f"Bağlantı zaman aşımına uğradı. {row['SWITCHNAME']} cihazına erişim mümkün olmayabilir.")
    except NetMikoAuthenticationException:
        print(f"Kimlik doğrulama hatası. {row['SWITCHNAME']} cihazındaki kullanıcı adı veya şifre hatalı olabilir.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {str(e)}")
