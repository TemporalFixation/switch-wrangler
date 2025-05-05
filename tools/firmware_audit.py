import csv
import os
import sys
from getpass import getpass
from tools.common import connect_switch, get_hostname, timestamp_string

username = input("Username: ")
password = getpass("Password: ")

# Optional CLI flag: --csv path/to/baseline.csv
baseline_map = {}
baseline_path = None

# Check for --csv flag
if "--csv" in sys.argv:
    try:
        idx = sys.argv.index("--csv") + 1
        baseline_path = sys.argv[idx]
    except IndexError:
        print("❌ Error: Missing CSV path after --csv")
        sys.exit(1)

if not baseline_path:
    answer = input("📋 Do you want to compare against a firmware baseline CSV? (y/N): ").strip().lower()
    if answer == 'y':
        baseline_path = input("🔍 Enter path to baseline CSV (format: model,version): ").strip()

if baseline_path:
    try:
        with open(baseline_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                model = row["model"].strip().lower()
                version = row["version"].strip().lower()
                baseline_map[model] = version
    except Exception as e:
        print(f"❌ Failed to load baseline: {e}")
        print("Proceeding without baseline comparison...")
        baseline_map = {}

# Prepare output CSV
output_dir = "audit_logs"
os.makedirs(output_dir, exist_ok=True)
report_path = os.path.join(output_dir, f"firmware_audit_{timestamp_string()}.csv")

with open("switches.txt") as f:
    switches = [line.strip() for line in f if line.strip()]

with open(report_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    headers = ["switch_ip", "hostname", "model", "firmware_version"]
    if baseline_map:
        headers.append("status")
    writer.writerow(headers)

    for ip in switches:
        print(f"\n🖥️ Auditing {ip}...")

        try:
            conn = connect_switch(ip, username, password)
            hostname = get_hostname(conn)
            version_output = conn.send_command("show version")
            conn.disconnect()

            model = "unknown"
            version = "unknown"

            for line in version_output.splitlines():
                if "Model number" in line or "Model Number" in line:
                    model = line.split(":")[-1].strip().lower()
                elif "System image file is" in line:
                    version = line.split("\"")[-2].strip().split("/")[-1].strip().lower()

            row = [ip, hostname, model, version]

            if baseline_map:
                expected = baseline_map.get(model)
                if not expected:
                    status = "unknown model"
                elif version == expected:
                    status = "ok"
                else:
                    status = f"mismatch (expected {expected})"
                row.append(status)
                print(f"{hostname}: {model}, {version} → {status}")
            else:
                print(f"{hostname}: {model}, {version}")

            writer.writerow(row)

        except Exception as e:
            print(f"❌ Failed to audit {ip}: {e}")
            err_row = [ip, "ERROR", "N/A", "N/A"]
            if baseline_map:
                err_row.append(str(e))
            writer.writerow(err_row)
