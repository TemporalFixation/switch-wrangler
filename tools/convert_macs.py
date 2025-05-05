import csv
from tools.common import normalize_mac

input_file = "convert-macs.csv"
output_file = "converted_macs.csv"
normalized_list = []

with open(input_file, newline="") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["original", "normalized"])

    for row in reader:
        if not row or not row[0].strip():
            continue

        original = row[0].strip()
        try:
            normalized = normalize_mac(original)
            normalized_list.append(normalized)
            writer.writerow([original, normalized])
            print(f"{original} → {normalized}")
        except Exception as e:
            print(f"❌ Failed to convert {original}: {e}")

# Ask if user wants to overwrite mac_addresses.txt
answer = input("\n📝 Overwrite mac_addresses.txt with the normalized MACs? (y/N): ").strip().lower()
if answer == 'y':
    try:
        with open("mac_addresses.txt", "w") as macfile:
            for mac in normalized_list:
                macfile.write(f"{mac}\n")
        print("✅ mac_addresses.txt has been updated.")
    except Exception as e:
        print(f"❌ Failed to write mac_addresses.txt: {e}")
else:
    print("⏭ Skipped updating mac_addresses.txt.")
