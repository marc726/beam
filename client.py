import socket

class Client:
    def __init__(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.is_connected = False

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.is_connected = True
        except Exception as e:
            print(e)
            self.is_connected = False
        return self.is_connected

    def disconnect_from_server(self):
        self.client_socket.close()
        self.is_connected = False