cat > wifi_setup.sh << 'EOF'
#!/bin/bash
echo "📶 WiFi Setup for Fake AP (No Root)"

# Enable WiFi hotspot mode (Termux workaround)
echo "1. Go to Android Settings > Network & Internet > Hotspot & Tethering"
echo "2. Enable WiFi Hotspot"
echo "3. Set SSID to: FREE-WIFI-2026"
echo "4. Set password: (leave empty if possible)"
echo "5. Return here and press Enter"

read -p "Hotspot enabled? "

# Setup IP forwarding
ip route add 192.168.43.0/24 dev wlan0
ifconfig wlan0 192.168.4.1 netmask 255.255.255.0 up

echo "✅ IP: 192.168.4.1"
echo "🔥 Run: python main.py"
EOF

chmod +x wifi_setup.sh
