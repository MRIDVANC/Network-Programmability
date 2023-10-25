from netmiko import ConnectHandler

# Cihaz konfigürasyonu
cisco_device = {
    'device_type': 'cisco_ios',
    'ip': 'your_switch_ip',
    'username': 'your_username',
    'password': 'your_password',
    'port': 22,  # SSH için 22, Telnet için 23
    'secret': 'enable_password',  # Gerekirse enable şifresi
}

# Cisco switch'e bağlan
net_connect = ConnectHandler(**cisco_device)
print("Bağlantı başarılı.")

# "show version" komutunu gönder
output = net_connect.send_command('show version')
print(output)

# Bağlantıyı kapat
net_connect.disconnect()
