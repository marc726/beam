import socket
from threading import Thread
from tkinter import filedialog, Tk
import os

# Increase Speed by raising buffer size to 8kb
BUFFER_SIZE = 8192

class Client:
    def __init__(self, host='localhost', port=12345, save_dir=''):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.save_dir = save_dir
        self.is_connected = False

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.is_connected = True
            # Inform the server that the client is ready for file transfer
            self.client_socket.sendall(b'READY_FOR_FILE')
            Thread(target=self.receive_file).start()
            return True
        except Exception as e:
            print(f'Failed to connect to the server: {e}')
            return False

    def disconnect_from_server(self):
        self.client_socket.close()
        self.is_connected = False

    def receive_file(self):
        try:
            # Receive filename
            filename = self.client_socket.recv(BUFFER_SIZE).decode().strip()
            if filename == 'No file selected.':
                print('Server did not select a file.')
                return
            
            # Receive file size
            file_size = int(self.client_socket.recv(BUFFER_SIZE).decode().strip())
            
            # Open the file
            file_path = os.path.join(self.save_dir, filename)
            received_size = 0
            with open(file_path, 'wb') as file:
                while received_size < file_size:
                    data = self.client_socket.recv(min(BUFFER_SIZE, file_size - received_size))
                    if not data:
                        break
                    received_size += len(data)
                    file.write(data)
                    self.print_progress_bar(received_size, file_size)
            print('\nFile received.')
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.disconnect_from_server()

    @staticmethod
    def print_progress_bar(completed, total):
        percent = int((completed / total) * 100)
        print(f"Progress: [{'#' * percent}{' ' * (100 - percent)}] {percent}%", end='\r')