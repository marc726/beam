import socket
import os
from tkinter import filedialog

# Increase Speed by raising buffer size to 8kb
BUFFER_SIZE = 8192

class Server:
    def __init__(self, save_dir='', host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse port
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.running = False

    def start(self):
        self.running = True
        print('Server is waiting for a connection...')
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f'Connected to {addr}')
                file_path = filedialog.askopenfilename()
                if file_path:
                    self.send_file(client_socket, file_path)
                else:
                    client_socket.sendall(b'No file selected.')
            except Exception as e:
                print(f"Error occurred: {e}")
            finally:
                client_socket.close()
        self.server_socket.close()

    def stop(self):
        self.running = False

    def send_file(self, client_socket, file_path):
        filename = os.path.basename(file_path)
        client_socket.sendall(filename.encode() + b'\n')

        file_size = os.path.getsize(file_path)
        bytes_sent = 0
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(BUFFER_SIZE)
                if not data:
                    break
                client_socket.sendall(data)
                bytes_sent += len(data)
                self.gui.update_progress_bar(bytes_sent, file_size)  # Update the server's progress bar.
        client_socket.sendall(b'EOF')  # Notify client of end of file
        print('File sent.')