import socket
import os

class Server:
    def __init__(self, save_dir='./', host='localhost', port=12345):
        self.save_dir = save_dir
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.running = False

    def start(self):
        self.running = True
        print('Server is listening...')
        while self.running:
            client_socket, addr = self.server_socket.accept()
            print(f'Connection from {addr}')
            with open(os.path.join(self.save_dir, 'received_file'), 'wb') as file:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)
            print('File received.')
            client_socket.close()
        self.server_socket.close()

    def stop(self):
        self.running = False