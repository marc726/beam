import socket
from threading import Thread
import time
from tkinter import filedialog, Tk
import os

#Increase Speed by raising buffer size to 8kb
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
        # Receive the first message from the server
        message = self.client_socket.recv(BUFFER_SIZE)

        if message == b'No file selected.':
            print('Server did not select a file.')
            return

        # If the message is not 'No file selected.', it is the filename
        filename = message.decode().strip()

        # Open the file
        file_path = os.path.join(self.save_dir, filename)
        with open(file_path, 'wb') as file:
            while True:
                data = self.client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                file.write(data)
        print('File received.')
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        self.disconnect_from_server()

    def disconnect_from_server(self):
        self.is_connected = False
        self.client_socket.close()