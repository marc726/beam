import socket
import os
from tkinter import filedialog

class Server:
    def __init__(self, host='localhost', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.running = False

    def start(self):
        self.running = True
        print('Server is waiting for a connection...')
        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f'Connected to {addr}')
            file_path = filedialog.askopenfilename()
            if file_path:
                self.send_file(client_socket, file_path)
            client_socket.close()
        self.server_socket.close()

    def stop(self):
        self.running = False

    def send_file(self, client_socket, file_path):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)
        print('File sent.')