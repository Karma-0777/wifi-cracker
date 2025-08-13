# Wi-Fi Cracker Script

> ⚠️ IMPORTANT: If the script uses a hardcoded path like `/home/user/`, 
> you **must replace `user` with your actual Linux username**. 
> Alternatively, the script can automatically detect your current user with `os.path.expanduser("~")`.

A Python3 script to automate cracking WPA/WPA2 Wi-Fi passwords using Hashcat and hcxtools.

---

## Features

- Automatically converts `.cap` files to `.hc22000` format.
- Cracks WPA/WPA2 handshakes using Hashcat.
- Allows selection of `.cap` files and wordlists.
- Extracts and displays only the SSID and password.
- Works on Linux with Python3.

---

## Requirements

- Python 3
- pip
- Hashcat
- hcxtools
- Linux system (Ubuntu/Debian recommended)

---

## Installation

Install dependencies:

```bash
sudo apt update -y
sudo apt install -y python3 python3-pip hashcat hcxtools
