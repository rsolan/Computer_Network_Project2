import socket
import sys
import threading
import os

def listen_for_shutdown(server_socket):
    global server_running
    while server_running:
        shutdown_command = input("Type 'shutdown' to stop the server: ")
        if shutdown_command.lower() == 'shutdown':
            print("Shutting down the server...")
            server_running = False
            try:
                # Create a temporary socket to connect to the server,
                # prompting it to exit the blocking accept call
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
                    temp_socket.connect(('localhost', port))
                    temp_socket.shutdown(socket.SHUT_RDWR)
            except Exception as e:
                print(f"Error shutting down server: {e}")
            server_socket.close()

def authenticate(client_socket):
    client_socket.send(b"Username: ")
    username = client_socket.recv(1024).decode().strip()
    client_socket.send(b"Password: ")
    password = client_socket.recv(1024).decode().strip()

    try:
        with open('users.txt', 'r') as file:
            for line in file:
                valid_username, valid_password = line.strip().split()
                if username == valid_username and password == valid_password:
                    client_socket.send(b"Authentication successful\n")
                    return True
        client_socket.send(b"Authentication failed\n")
        return False
    except FileNotFoundError:
        print("The users.txt file was not found.")
        client_socket.send(b"Server error: missing users file.\n")
        return False

def handle_file_upload(client_socket):
    client_socket.send(b"Filename: ")
    filename = client_socket.recv(1024).decode().strip()
    with open("new" + filename, 'wb') as f:
        client_socket.send(b"Start sending the file.")
        while True:
            data = client_socket.recv(1024)
            if data.endswith(b"EOF"):
                f.write(data[:-3])
                break
            f.write(data)
    client_socket.send(b"File uploaded successfully.\n")
    ack = client_socket.recv(1024).decode().strip()

def handle_file_download(client_socket):
    client_socket.send(b"Filename: ")
    filename = client_socket.recv(1024).decode().strip()

    try:
        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    client_socket.send(b"EOF")
                    break
                client_socket.send(bytes_read)
        ack = client_socket.recv(1024).decode().strip()
    except Exception as e:
        print(f"Error sending file: {e}")
        client_socket.send(b"Error in file transfer.\n")

# handle multiple client connections concurrently. The handle_client function is executed in a separate thread for each client.
def handle_client(client_socket):
    try:
        if not authenticate(client_socket):
            print("Authentication failed.")
            client_socket.close()
            return

        while True:
            client_socket.send(b"Enter command (get/upload/exit): ")
            command = client_socket.recv(1024).decode().strip()

            if command.lower() == 'exit':
                print("Client requested to close the connection....")
                print("Connection closed successfully.")
                break
            elif command.lower().startswith('upload'):
                handle_file_upload(client_socket)
            elif command.lower().startswith('get'):
                handle_file_download(client_socket)
            else:
                client_socket.send(b"Invalid command.\n")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server(port):
    global server_running
    server_running = True

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    # Start the shutdown listener thread
    shutdown_thread = threading.Thread(target=listen_for_shutdown, args=(server_socket,))
    shutdown_thread.start()

    try:
        while server_running:
            client_socket, addr = server_socket.accept()
            if server_running:
                print(f"Accepted connection from {addr}")
                # Pass the client socket to handle_client in a separate thread
                client_thread = threading.Thread(target=handle_client, args=(client_socket,))
                client_thread.start()
            else:
                client_socket.close()
    except Exception as e:
        print(f"Server stopped: {e}")
    finally:
        server_socket.close()
        os._exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = int(sys.argv[1])

    start_server(port)
