import socket

HOST = "127.0.0.1"
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(1024)
print(data.decode("utf-8"))

with open('received_file', 'wb') as file:
    while True:
        data = s.recv(1024)
        if not data:
            break
        file.write(data)

s.close()