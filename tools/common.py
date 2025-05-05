from netmiko import ConnectHandler
from datetime import datetime

def connect_switch(ip, username, password):
    device = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": username,
        "password": password,
    }
    return ConnectHandler(**device)

def get_hostname(conn):
    output = conn.send_command("show run | include hostname")
    return output.strip().split(" ")[-1] if "hostname" in output else "unknown"

def normalize_mac(mac):
    mac = mac.lower().replace("-", "").replace(":", "").replace(".", "")
    return ".".join([mac[i:i+4] for i in range(0, 12, 4)])

def timestamp_string():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
