Introduction
This project extends the previous FTP client-server application by introducing multi-threading to the
server component. The primary objective is to enhance the server's capability to handle multiple client
connections concurrently without blocking other clients. The application retains its original
functionalities, including file uploads and downloads in chunk-based transfers, but now supports
concurrent operations for improved efficiency and user experience.


Implementation Details
Programming Environment
● Programming Language: Python
● Operating System: Cross-platform (Windows, macOS, Linux)
● Tools: Any text editor or IDE that supports Python (Visual Studio Code)

Application Structure
The application comprises two main components: ftp_server.py and ftp_client.py.

Server (ftp_server.py)
The server program has been enhanced to utilize multi-threading, allowing it to handle multiple client
connections concurrently. It still manages client authentication and processes commands for file uploads
and downloads, with the added capability of supporting simultaneous operations from different clients.

Key Features:
● Listens on a specified port for client connections and supports multi-threading.
● Authenticates users against credentials stored in users.txt.
● Supports file uploads and downloads with chunk-based file transfer in a multi-threaded
environment.
● Implements a clean shutdown command.

Client (ftp_client.py)
The client program remains unchanged and connects to the server using the server's IP address and port
number. It allows the user to execute commands to upload or download files and supports a clean exit
command to terminate the connection gracefully.

Key Features:
● Connects to the server using the provided IP address and port.
● Authenticates the user.
● Allows file uploads and downloads.
● Supports a clean exit from the application.

File Transfer Mechanism
File transfers continue to be conducted in chunks of 1KB to manage large files efficiently. The
multi-threaded server handles concurrent file transfers from multiple clients without blocking other
clients, ensuring efficient utilization of resources.

Clean Shutdown
The server retains the clean shutdown mechanism, allowing it to shut down gracefully upon receiving a
shutdown command from the server's console, even when serving multiple clients.

Testing
The application was tested by simulating concurrent download and upload processes from a number of
clients. The tests confirmed that the application handles concurrent file transfers reliably, manages
chunking correctly, and renames files with the prefix "new" to prevent overwriting original files.


Conclusion
This project successfully extends the initial FTP client-server application by incorporating multi-threading
to enhance the server's concurrency capabilities. The application maintains its core functionalities while
adding the ability to serve multiple clients concurrently, thereby improving efficiency and user experience
in file transfers between clients and the server
