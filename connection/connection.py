from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException
cisco_device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.101',
    'username': 'admin',
    'password': 'Turkcell!2023',
    'port': 22,
}

try:
    # Cisco switch'e bağlan
    net_connect = ConnectHandler(**cisco_device)
    print("Bağlantı başarılı.")

    # "show interfaces" komutunu gönder ve sonucunu al
    output = net_connect.send_command('show interfaces')
    print("show interfaces komutunun sonucu:\n")
    print(output)

    # Bağlantıyı kapat
    net_connect.disconnect()

except NetMikoTimeoutException:
    print("Bağlantı zaman aşımına uğradı. Cihaz erişimi mümkün olmayabilir.")
except NetMikoAuthenticationException:
    print("Kimlik doğrulama hatası. Kullanıcı adı veya şifre hatalı olabilir.")
except Exception as e:
    print(f"Beklenmeyen bir hata oluştu: {str(e)}")

# İkinci bağlantı yapılıyor, yukarıdaki bağlantının ardından eklenen kod bloğu
net_connect = ConnectHandler(**cisco_device)
print("Bağlantı başarılı.")

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
