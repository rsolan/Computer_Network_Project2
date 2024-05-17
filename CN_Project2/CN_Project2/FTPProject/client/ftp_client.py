import socket
import os
import sys

# handle file uploads and downloads in 1K-byte chunks
def send_file(s, filename):
    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                s.sendall(b"EOF")    #the end-of-file (EOF) signaling
                break
            s.sendall(bytes_read)

def receive_file(s, filename):
    with open(filename, 'wb') as f:
        while True:
            bytes_received = s.recv(1024)
            if bytes_received.endswith(b"EOF"):
                f.write(bytes_received[:-3])
                break
            f.write(bytes_received)
    s.send(b"ACK")

def connect_to_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def authenticate(s):
    username = input(s.recv(1024).decode())
    s.send(username.encode())
    password = input(s.recv(1024).decode())
    s.send(password.encode())
    response = s.recv(1024).decode()
    print(response)
    return "Authentication successful" in response

def client(host, port):
    s = connect_to_server(host, port)
    if not authenticate(s):
        print("Authentication failed.")
        s.close()
        return

    while True:
        command = input("Enter command (get/upload/exit): ").strip().lower()
        if command == 'exit':
            s.send(b"exit")
            s.close()
            break
        elif command.startswith('upload'):
            s.send(command.encode())
            filename = input("Enter filename to upload: ").strip()
            if not os.path.isfile(filename):
                print("File does not exist.")
                continue
            s.send(filename.encode())
            send_file(s, filename)
            print(s.recv(1024).decode())
            print("File uploaded successfully.")
            s.send(b"ACK")
        elif command.startswith('get'):
            s.send(command.encode())
            filename = input("Enter filename to download: ").strip()
            s.send(filename.encode())
            receive_file(s, "new" + filename)
            print("File downloaded successfully.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    client(host, port)
