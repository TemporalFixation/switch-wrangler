# 🔌 Switch Wrangler

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Cisco%20IOS-lightgrey.svg)
![Status](https://img.shields.io/badge/status-internal--tool-orange.svg)

Switch Wrangler is a modular Python toolkit designed to help you manage older Cisco switches (like the Catalyst 2960 series) more efficiently. It provides simple, CLI-driven tools for identifying, auditing, and updating switch configurations across a network — no enterprise software or complex platforms required.

## 🧰 Features

- 🔍 **Find Devices by MAC** – Locate which switch and port a MAC address is connected to
- 💥 **Bounce Ports** – Find and optionally shut/no-shut ports connected to target devices
- 🧠 **Firmware Audit** – Compare current firmware versions to a known-good baseline
- 💾 **Backup Configs** – Save `show run` for each switch into timestamped files
- 🔁 **MAC Address Converter** – Normalize MAC address formats into Cisco-friendly style
- 📄 **CSV Logging** – All tools log to CSV for tracking, auditing, or ticketing

---

## 📁 Repo Structure

```
switch-wrangler/
├── tools/
│   ├── bounce_cameras.py         # Bounce ports based on MAC
│   ├── backup_configs.py         # Backup show running-config
│   ├── firmware_audit.py         # Compare IOS firmware to baseline
│   ├── find_devices.py           # Report switch+port for each MAC
│   ├── convert_macs.py           # Normalize MAC formats
│   └── common.py                 # Shared functions (connect, normalize, etc.)
├── switches.txt                  # List of switch IPs (one per line)
├── mac_addresses.txt             # Target MACs (Cisco format)
├── convert-macs.csv              # Raw MACs to normalize
├── converted_macs.csv            # Output of converted MACs
├── firmware_baseline.csv         # Optional firmware baseline (model,version)
├── backups/                      # Saved configs
├── audit_logs/                   # Firmware audit results
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Install Python 3

Make sure Python 3.x is installed and added to your PATH.

### 2. Create a virtual environment

```bash
python -m venv .env
. .env/Scripts/activate  # Windows
pip install -r requirements.txt
```

### 3. Install dependencies

```text
netmiko
```

---

## 🚀 Usage

### 🔍 Find Devices by MAC

```bash
python tools/find_devices.py
```

- Reads MACs from `mac_addresses.txt`
- Scans switches in `switches.txt`
- Outputs `device_locations_<date>.csv`

---

### 💥 Bounce Ports

```bash
python tools/bounce_cameras.py
```

- Finds each MAC address, shows VLAN + port
- Prompts before shutting/no-shutting each port
- Logs results to `camera_port_log_<date>.csv`

---

### 💾 Backup Configs

```bash
python tools/backup_configs.py
```

- Logs into each switch in `switches.txt`
- Runs `show running-config`
- Saves to `backups/<hostname>_<ip>_<date>.txt`

---

### 🧠 Firmware Audit

```bash
python tools/firmware_audit.py
```

- Prompts whether to load a firmware baseline
- If yes: compares IOS version per switch to known baseline
- If no: just logs model + version
- Outputs to `audit_logs/firmware_audit_<date>.csv`

---

### 🔁 Convert MAC Addresses

```bash
python tools/convert_macs.py
```

- Reads MACs from `convert-macs.csv`
- Outputs normalized MACs to `converted_macs.csv`
- Converts formats like `xx:xx:xx:xx:xx:xx` → `xxxx.yyyy.zzzz`

---

## 🛠 Example Input Files

### `convert-macs.csv`
```
00:11:22:33:44:55
aa-bb-cc-dd-ee-ff
1122.3344.5566
```

### `mac_addresses.txt`
```
aaaa.bbbb.cccc
1122.3344.5566
```

### `switches.txt`
```
192.168.1.10
192.168.1.11
```

### `firmware_baseline.csv`
```csv
model,version
ws-c2960x-48fps-l,c2960x-universalk9-mz.152-4.e7
ws-c2960-24tt-l,c2960-lanbasek9-mz.150-2.se11
```

---

## 🛠 Example Output Files

### `converted_macs.csv`
```
original,normalized
00:11:22:33:44:55,0011.2233.4455
aa-bb-cc-dd-ee-ff,aabb.ccdd.eeff
1122.3344.5566,1122.3344.5566

```


## 👷 Roadmap

- TFTP-based config backup (future)
- Git-based config diff & rollback (future)
- Web dashboard or Flask UI wrapper (maybe)

---

## 📜 License

MIT License. Use at your own risk. Don’t `no shut` yourself out of the network.

---

## 🤘 Author

Kris F | Built with pain, coffee, and 80 old security cameras
