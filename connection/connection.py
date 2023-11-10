from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException
from kripto import encrypt_decrypt_password, get_key


def connect_to_switch(ip_address):
    encrypted_password = encrypt_decrypt_password(ip_address)
    get_key("192.168.1.103")
    get_key("192.168.1.104")
    switch_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address,
        'username': 'admin',
        'password': encrypted_password,  # Şifre yerine şifrelenmiş hali kullanılıyor
        'port': 22,
    }

    try:
        # Switch'e bağlan
        net_connect = ConnectHandler(**switch_device)
        print(f"Bağlantı başarılı. {ip_address} switch'ine bağlandınız.")

        # "show interfaces" komutunu gönder ve sonucunu al
        output = net_connect.send_command('show interfaces')
        print("show interfaces komutunun sonucu:\n")
        print(output)

        # Diğer işlemler devam ediyor
        # Örnek 1: "show interfaces" komutunu gönder ve sonucunu al
        output = net_connect.send_command('show interface status')
        print("show interface status komutunun sonucu:\n")
        print(output)

        # Örnek 2: "show ip route" komutunu gönder ve sonucunu al
        output2 = net_connect.send_command('show lldp neighbors')
        print("\nshow lldp komutunun sonucu:\n")
        print(output2)

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

        # Bağlantıyı kapat
        net_connect.disconnect()

    except NetMikoTimeoutException:
        print("Bağlantı zaman aşımına uğradı. Cihaz erişimi mümkün olmayabilir.")
    except NetMikoAuthenticationException:
        print("Kimlik doğrulama hatası. Kullanıcı adı veya şifre hatalı olabilir.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {str(e)}")


# Kullanıcıya hangi switch için işlem yapmak istediğini sormak
while True:
    switch_choice = input(
        "Hangi switch için işlem yapmak istiyorsunuz? (Q/q to exit, 1 for 192.168.1.103, "
        "2 for 192.168.1.104): ").lower()

    if switch_choice == 'q':
        break
    elif switch_choice == '1':
        connect_to_switch(ip_address='192.168.1.103')
    elif switch_choice == '2':
        connect_to_switch(ip_address='192.168.1.104')
    else:
        print("Geçersiz giriş. Lütfen doğru bir switch numarası girin.")
