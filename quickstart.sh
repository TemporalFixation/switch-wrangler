#!/bin/bash

echo "📦 Creating virtual environment..."
python3 -m venv .env
source .env/bin/activate

echo "⬇️ Installing dependencies..."
pip install -r requirements.txt

echo "📄 Files detected:"
echo "- MACs: $(wc -l < mac_addresses.txt) entries"
echo "- Switches: $(wc -l < switches.txt) switches"

echo "🔍 Running MAC scan (find_devices.py)..."
python tools/find_devices.py

echo "✅ Done. Output saved to device_locations_*.csv"
