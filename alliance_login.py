#!/usr/bin/env python3
"""
Alliance Broadband Auto Login - Monitors connection every 5 minutes
Automatically reconnects if disconnected
"""

import requests
import sys
import time
from datetime import datetime

# Your credentials - CHANGE THESE
USERNAME = "CHANGEME"
PASSWORD = "CHANGEME"

# Alliance Broadband gateways
GATEWAYS = [
    "http://10.254.254.2/0/up/",
    "http://10.254.254.46/0/up/",
    "http://10.254.254.8/0/up/",
    "http://10.254.254.39/0/up/",
    "http://10.254.254.16/0/up/"
]

# Check interval (5 minutes)
CHECK_INTERVAL = 300  # seconds

def log(message):
    """Print message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

#def check_internet():
 #   """Check if internet is working"""
  #  test_urls = [
   #     "http://www.google.com",
    #    "http://www.cloudflare.com",
     #   "http://1.1.1.1"
    #]
#    
 #   for url in test_urls:
  #      try:
   #         response = requests.get(url, timeout=3)
    #        if response.status_code == 200:
    #           return True
     #  except:
      #      continue
#    
 #   return False

def check_internet():
    """Check if internet is working using ping"""
    import subprocess
    
    test_ips = ["8.8.8.8", "1.1.1.1"]
    
    for ip in test_ips:
        try:
            # Ping with 1 packet, 2 second timeout
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '2', ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if result.returncode == 0:
                return True
        except:
            continue
    
    return False

def login():
    """Login to Alliance Broadband"""
    
    log("Attempting to login...")
    
    # Try each gateway
    for gateway in GATEWAYS:
        try:
            data = {
                'user': USERNAME,
                'pass': PASSWORD,
                'login': 'Login'
            }
            
            response = requests.post(gateway, data=data, timeout=5)
            
            if response.status_code == 200:
                log(f"✓ Login successful via {gateway}")
                return True
                
        except:
            continue
    
    return False

def keep_connected():
    """Main loop - keeps checking and reconnecting"""
    
    log("Alliance Broadband Auto Login Monitor Started")
    log(f"Checking connection every {CHECK_INTERVAL // 60} minutes")
    log("-" * 60)
    
    while True:
        try:
            # Check if internet is working
            if check_internet():
                log("✓ Internet connected")
            else:
                log("✗ Internet disconnected - Reconnecting...")
                
                # Keep trying to login until successful
                attempt = 1
                while True:
                    log(f"Login attempt #{attempt}")
                    
                    if login():
                        # Verify connection
                        time.sleep(2)
                        if check_internet():
                            log("✓ Successfully reconnected!")
                            break
                    
                    attempt += 1
                    log(f"Retrying in 10 seconds...")
                    time.sleep(10)
            
            # Wait before next check
            log(f"Next check in {CHECK_INTERVAL // 60} minutes...")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            log("Stopped by user")
            sys.exit(0)
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Check if credentials are set
    if USERNAME == "your_username" or PASSWORD == "your_password":
        print("ERROR: Please edit the script and add your credentials")
        print("Edit USERNAME and PASSWORD at the top of the script")
        sys.exit(1)
    
    keep_connected()
