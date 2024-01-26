import socket
import threading
import os
import logging
from tkinter import Tk, Text, Button, END, Scrollbar, VERTICAL, RIGHT, Y
from tkinter import LEFT

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_server(port, log):
    setup_logging()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        logging.info(f"Server listening on port {port}")
        update_log(log, f"Server started on port {port}")
    except Exception as e:
        logging.error(f"Error starting server: {e}")
        update_log(log, f"Error: {e}")
        return

    while True:
        try:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr, log))
            thread.daemon = True
            thread.start()
        except Exception as e:
            logging.error(f"Error accepting connections: {e}")
            update_log(log, f"Error: {e}")

def handle_client(client_socket, addr, log):
    logging.info(f"Connection from {addr} has been established.")
    update_log(log, f"Connection from {addr}")
    with client_socket:
        try:
            raw_filename = client_socket.recv(1024)
            filename = raw_filename.decode('utf-8').rstrip('\x00')  # Handle decoding errors
            if not filename:
                raise ValueError("No filename received")
            safe_filename = os.path.basename(filename)  # Avoid directory traversal attacks
            with open(safe_filename, 'wb') as f:
                while True:
                    bytes_read = client_socket.recv(4096)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            logging.info(f"File {filename} received from {addr}.")
            update_log(log, f"Received {filename} from {addr}")
        except Exception as e:
            logging.error(f"Error receiving file: {e}")
            update_log(log, f"Error: {e}")

def update_log(log_widget, message):
    log_widget.config(state='normal')
    log_widget.insert(END, message + "\n")
    log_widget.config(state='disabled')
    log_widget.see(END)

def main():
    root = Tk()
    root.title("File Transfer Server")

    log = Text(root, state='disabled', height=20, width=70)
    log.pack(side=LEFT, fill=Y)

    scrollbar = Scrollbar(root, orient=VERTICAL, command=log.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    log['yscrollcommand'] = scrollbar.set

    start_button = Button(root, text="Start Server", command=lambda: threading.Thread(target=start_server, args=(12345, log)).start())
    start_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
