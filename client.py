import socket
from tkinter import Tk, Button, Entry, Label, filedialog

def send_file(filename, host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(f"{filename}".encode())

    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)

    client_socket.close()

def select_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, 'end')
    entry.insert(0, filename)

def main():
    root = Tk()
    root.title("File Transfer Client")

    entry = Entry(root, width=50)
    entry.pack()

    browse_button = Button(root, text="Browse", command=lambda: select_file(entry))
    browse_button.pack()

    send_button = Button(root, text="Send File", command=lambda: send_file(entry.get(), '127.0.0.1', 12345))
    send_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
