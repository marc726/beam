import socket
import logging
import os
from tkinter import Tk, Button, Entry, Label, filedialog, Text, END, messagebox

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_file(filename, host, port, log):
    setup_logging()
    if not filename:
        logging.warning("No file selected")
        update_log(log, "No file selected")
        return

    if not os.path.isfile(filename):
        logging.warning("Selected file does not exist")
        update_log(log, "File does not exist")
        return
    
    if '\x00' in os.path.basename(filename):
        raise ValueError("Filename contains null characters")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        basename = os.path.basename(filename)
        client_socket.send(len(basename).to_bytes(4, 'big'))  # Send length of filename
        client_socket.send(basename.encode('utf-8'))  # Send filename

        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)

        update_log(log, f"File {filename} sent to {host}:{port}")
        logging.info(f"File {filename} sent to {host}:{port}")
    except Exception as e:
        logging.error(f"Error sending file: {e}")
        update_log(log, f"Error: {e}")
        messagebox.showerror("Error", f"Could not send file: {e}")
    finally:
        client_socket.close()

def select_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, 'end')
    entry.insert(0, filename)

def update_log(log_widget, message):
    log_widget.config(state='normal')
    log_widget.insert(END, message + "\n")
    log_widget.config(state='disabled')
    log_widget.see(END)

def main():
    root = Tk()
    root.title("File Transfer Client")

    entry = Entry(root, width=50)
    entry.pack()

    browse_button = Button(root, text="Browse", command=lambda: select_file(entry))
    browse_button.pack()

    log = Text(root, state='disabled', height=10, width=50)
    log.pack()

    send_button = Button(root, text="Send File", command=lambda: send_file(entry.get(), '127.0.0.1', 12345, log))
    send_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
