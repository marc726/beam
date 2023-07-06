import socket
from threading import Thread
import time

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
            Thread(target=self.receive_file).start()
            return True
        except socket.error:
            return False

    def disconnect_from_server(self):
        self.client_socket.close()
        self.is_connected = False

    def receive_file(self):
        with open(self.save_dir + '/received_file', 'wb') as file:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print('File received.')


    def receive_file(self):
        unique_filename = self.save_dir + '/received_file_' + str(int(time.time()))
        with open(unique_filename, 'wb') as file:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print('File received.')

    def disconnect_from_server(self):
        self.is_connected = False
        self.client_socket.close()

