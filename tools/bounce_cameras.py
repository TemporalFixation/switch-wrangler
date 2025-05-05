from netmiko import ConnectHandler
from getpass import getpass
import csv
from tools.common import connect_switch, get_hostname, normalize_mac, timestamp_string

username = input("Username: ")
password = getpass("Password: ")

# Load and normalize MACs
with open("mac_addresses.txt") as f:
    mac_list = [normalize_mac(line.strip()) for line in f if line.strip()]

# Load switches
with open("switches.txt") as f:
    switches = [line.strip() for line in f if line.strip()]

# Prepare CSV log file
logfile = f"camera_port_log_{timestamp_string()}.csv"

with open(logfile, mode="w", newline="") as csvfile:
    logwriter = csv.writer(csvfile)
    logwriter.writerow(["timestamp", "switch_ip", "hostname", "mac_address", "vlan", "port", "action"])

    for ip in switches:
        print(f"\n📡 Connecting to {ip}...")

        try:
            conn = connect_switch(ip, username, password)
            hostname = get_hostname(conn)
            mac_table = conn.send_command("show mac address-table", use_textfsm=True)

            if not isinstance(mac_table, list):
                print("⚠ Unexpected output format. Skipping switch.")
                conn.disconnect()
                continue

            found_ports = []

            for entry in mac_table:
                mac = entry.get("destination_address", "").lower()
                port = entry.get("destination_port", "")
                vlan = entry.get("vlan", "")

                if mac in mac_list:
                    print(f"✔ Found {mac} on {hostname} ({ip}) VLAN {vlan} Port {port}")
                    found_ports.append(port)

                    action = "skipped"
                    answer = input(f"➡ Bounce port {port} on {hostname}? (y/N): ").strip().lower()
                    if answer == 'y':
                        print(f"🔌 Bouncing {port}...")
                        conn.send_config_set([
                            f"interface {port}",
                            "shutdown",
                            "no shutdown"
                        ])
                        print(f"✅ Port {port} reset complete.")
                        action = "bounced"
                    else:
                        print(f"⏭ Skipped {port}")

                    logwriter.writerow([
                        timestamp_string(),
                        ip,
                        hostname,
                        mac,
                        vlan,
                        port,
                        action
                    ])

            if not found_ports:
                print(f"— No target MACs found on {hostname} ({ip})")

            conn.disconnect()

        except Exception as e:
            print(f"❌ Error on {ip}: {e}")
