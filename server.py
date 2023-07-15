import socket
import os
import tkinter as tk
from tkinter import filedialog
import threading

HOST = "127.0.0.1"
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

def send_file(client_socket, file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1024)
                client_socket.send(data)
                if not data:
                    break
    else:
        client_socket.send(b'File does not exist')

def serverToClientWindow():
    root = tk.Tk()
    root.title("Send Files")
    root.minsize(300,300)
    root.maxsize(400,400)
    root.mainloop()

def server_loop():
    while True:
        clientSocket, address = s.accept()
        print(f"Connection established from address: {address}")
        clientSocket.send(bytes("Welcome to the server", "utf-8"))
        # Create and show the GUI window after a client has connected
        gui_thread = threading.Thread(target=serverToClientWindow)
        gui_thread.start()
        file_path = filedialog.askopenfilename()  # open the dialog to choose file
        if file_path:  # if a file is selected
            send_file(clientSocket, file_path)
        clientSocket.close()

# Create threads for server
server_thread = threading.Thread(target=server_loop)
server_thread.start()