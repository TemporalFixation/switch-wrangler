from netmiko import ConnectHandler
from getpass import getpass
from tools.common import connect_switch, get_hostname, normalize_mac, timestamp_string
import csv

username = input("Username: ")
password = getpass("Password: ")

# Load and normalize MACs
with open("mac_addresses.txt") as f:
    macs = [normalize_mac(line.strip()) for line in f if line.strip()]

# Load switch IPs
with open("switches.txt") as f:
    switches = [line.strip() for line in f if line.strip()]

# Set up CSV logging
timestamp = timestamp_string()
outfile = f"device_locations_{timestamp}.csv"

with open(outfile, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["switch_ip", "hostname", "mac_address", "vlan", "port"])

    for ip in switches:
        print(f"\n🔍 Scanning {ip}...")
        try:
            conn = connect_switch(ip, username, password)
            hostname = get_hostname(conn)
            mac_table = conn.send_command("show mac address-table", use_textfsm=True)
            conn.disconnect()

            if not isinstance(mac_table, list):
                print(f"⚠ Unexpected output from {ip}")
                continue

            found = 0
            for entry in mac_table:
                mac = entry["destination_address"].lower()
                if mac in macs:
                    vlan = entry["vlan"]
                    port = entry["destination_port"]
                    print(f"✔ Found {mac} on {hostname} ({ip}) VLAN {vlan} Port {port}")
                    writer.writerow([ip, hostname, mac, vlan, port])
                    found += 1

            if found == 0:
                print(f"— No target MACs found on {hostname} ({ip})")

        except Exception as e:
            print(f"❌ Error on {ip}: {e}")
