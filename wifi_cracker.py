#!/usr/bin/env python3
import os
import sys
import subprocess

def run_cmd(cmd):
    print(f"[+] Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[!] Command failed: {cmd}")
        sys.exit(1)

# 1. Check arguments
if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <capture.cap> <wordlist.txt>")
    sys.exit(1)

cap_file = sys.argv[1]
wordlist = sys.argv[2]

# 2. Install dependencies
print("[+] Installing dependencies (Python3, pip, Hashcat, hcxtools)...")
run_cmd("sudo apt update -y && sudo apt install -y python3 python3-pip hashcat hcxtools")

# 3. Convert .cap to .hc22000
hc22000_file = cap_file.replace(".cap", ".hc22000")
print(f"[+] Converting {cap_file} to {hc22000_file}...")
run_cmd(f"hcxpcapngtool -o {hc22000_file} {cap_file}")

# 4. Crack the handshake
print(f"[+] Starting Hashcat with {wordlist}...")
hashcat_cmd = f"hashcat -m 22000 -a 0 {hc22000_file} {wordlist} --quiet --potfile-disable"
result = subprocess.run(hashcat_cmd, shell=True, capture_output=True, text=True)

# 5. Extract only SSID and password
lines = result.stdout.strip().split("\n")
for line in lines:
    if ":" in line:
        parts = line.split(":")
        if len(parts) >= 5:
            ssid = parts[3]
            password = parts[4]
            print(f"\n[✓] SSID: {ssid}\n[✓] Password: {password}")
            break
else:
    print("[!] No password found.")
