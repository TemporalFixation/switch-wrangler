def connect_switch(ip, username, password):
    from netmiko import ConnectHandler
    return ConnectHandler({
        "device_type": "cisco_ios",
        "ip": ip,
        "username": username,
        "password": password,
    })

def get_hostname(conn):
    output = conn.send_command("show run | include hostname")
    return output.strip().split(" ")[-1] if "hostname" in output else "unknown"

def timestamp_string():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def clean_filename(hostname):
    return hostname.replace(" ", "_").replace("/", "_")
