import re
from netmiko import ConnectHandler

def get_lldp_info(ip, username, password):
    device = {
        'device_type': 'linux',
        'ip': ip,
        'username': username,
        'password': password,
    }

    try:
        with ConnectHandler(**device) as ssh:
            # LLDP bilgilerini al
            lldp_output = ssh.send_command("lldpcli show neighbors")

            # Düzenli ifadelerle verileri filtrele
            matches = re.finditer(r'Interface:\s+(\S+).*?ChassisID:\s+(.*?)\s+SysName:\s+(.*?)\s+MgmtIP:\s+(.*?)\s+MgmtIface:\s+(\d+).*?PortID:\s+(.*?)\s+PortDescr:\s+(.*?)\s+', lldp_output, re.DOTALL)

            # Her eşleşen veri için istenilen bilgileri ekrana bas
            for match in matches:
                interface = match.group(1)
                chassis_id = match.group(2)
                sys_name = match.group(3)
                mgmt_ip = match.group(4)
                mgmt_iface = match.group(5)
                port_id = match.group(6)
                port_descr = match.group(7)

                print(f"\nInterface: {interface}")
                print(f"ChassisID: {chassis_id}")
                print(f"SysName: {sys_name}")
                print(f"MgmtIP: {mgmt_ip}")
                print(f"MgmtIface: {mgmt_iface}")
                print(f"PortID: {port_id}")
                print(f"PortDescr: {port_descr}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ip_address = "192.168.122.201"
    username = "root"
    password = "Test123"

    get_lldp_info(ip_address, username, password)
