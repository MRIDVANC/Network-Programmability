from netmiko import ConnectHandler

# Cihaz konfigürasyonu
cisco_device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.101',
    'username': 'admin',
    'password': 'Turkcell!2023',
    'port': 22,  # SSH için 22, Telnet için 23
    # 'secret': 'enable_password',  # Gerekirse enable şifresi
}

# Cisco switch'e bağlan
net_connect = ConnectHandler(**cisco_device)
print("Bağlantı başarılı.")

# Örnek 1: "show interfaces" komutunu gönder ve sonucunu al
output = net_connect.send_command('show interface status')
print("show interface status komutunun sonucu:\n")
print(output)

# Örnek 2: "show ip route" komutunu gönder ve sonucunu al
output2 = net_connect.send_command('show routing summary vrf default ')
print("\nshow ip route komutunun sonucu:\n")
print(output2)

# Örnek 3: Cihazın konfigürasyonunu değiştirme
config_commands = [
    'conf term',
    'interface ethernet 1/1',
    'description configDeneme',
    'no shutdown'
]
output3 = net_connect.send_config_set(config_commands)
print("\nKonfigürasyon değişikliği sonucu:\n")
output3 = net_connect.send_command('show run interface ethernet 1/1 ')
print(output3)

# Bağlantıyı kapat
net_connect.disconnect()
