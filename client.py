import socket
from threading import Thread
from tkinter import filedialog, Tk
import os

# Increase Speed by raising buffer size to 8kb
BUFFER_SIZE = 8192

class Client:
    def __init__(self, host='localhost', port=12345, save_dir='', gui=None):  # Add a 'gui' parameter with a default value of None.
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.save_dir = save_dir
        self.gui = gui  # Assign the 'gui' parameter to an instance variable.
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
        
        print(f'Client.gui: {self.gui}')  # Debug print

    def disconnect_from_server(self):
        self.client_socket.close()
        self.is_connected = False

    def receive_file(self):
        try:
            # Receive the first message from the server
            message = self.client_socket.recv(BUFFER_SIZE)

            if message == b'No file selected.':
                print('Server did not select a file.')
                return

            # If the message is not 'No file selected.', it is the filename
            filename = message.decode().strip()

            # Receive file size
            file_size = ""
            while True:
                char = self.client_socket.recv(1).decode()
                if char == '\n':
                    break
                file_size += char
            file_size = int(file_size)

            # Create a new file in the current directory
            with open(filename, 'wb') as file:
                bytes_received = 0
                while bytes_received < file_size:
                    bytes_to_read = min(BUFFER_SIZE, file_size - bytes_received)
                    data = self.client_socket.recv(bytes_to_read)
                    if not data:
                        break
                    file.write(data)
                    bytes_received += len(data)
                    if self.gui:  # Check if the gui instance was provided
                        self.gui.update_progress_bar(bytes_received, file_size)
            print('File received.')
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.disconnect_from_server()

        print(f'Client.gui: {self.gui}')  # Debug print

    @staticmethod
    def print_progress_bar(completed, total):
        percent = int((completed / total) * 100)
        print(f"Progress: [{'#' * percent}{' ' * (100 - percent)}] {percent}%", end='\r')