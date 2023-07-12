import tkinter as tk
from tkinter import filedialog
from threading import Thread
from client import Client
from server import Server
from tkinter import filedialog, messagebox, ttk, Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("File Transfer")

        self.server_port_label = tk.Label(self, text="Server Port:")
        self.server_port_label.pack()

        self.server_port_entry = tk.Entry(self)
        self.server_port_entry.pack()

        self.start_server_button = tk.Button(self, text="Start Server", command=self.start_server)
        self.start_server_button.pack()

        self.stop_server_button = tk.Button(self, text="End Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_server_button.pack()

        self.ip_label = tk.Label(self, text="IP address:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(self)
        self.ip_entry.pack()

        self.port_label = tk.Label(self, text="Port:")
        self.port_label.pack()

        self.port_entry = tk.Entry(self)
        self.port_entry.pack()

        self.connect_button = tk.Button(self, text="Connect to Server", command=self.connect_to_server)
        self.connect_button.pack()

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

        self.save_dir_button = tk.Button(self, text="Select Save Directory", command=self.select_save_dir)
        self.save_dir_button.pack()
        
        self.save_dir_label = tk.Label(self, text="Save Directory:")
        self.save_dir_label.pack()

         # Add progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress.pack()

        self.client = None
        self.server = None
        self.save_dir = tk.StringVar()

        self.save_dir = filedialog.askdirectory()  # Prompt the user to select a directory

        while not self.save_dir:  # Keep prompting until a directory is selected
            messagebox.showinfo("Select Directory", "You must select a directory to save files!")
            self.save_dir = filedialog.askdirectory()
        
        self.save_dir_label.config(text=f"Save Directory: {self.save_dir}")

    def start_progress(self, max_val):
        self.progress["value"] = 0
        self.progress["maximum"] = max_val
    
    def update_progress_bar(self, completed, total):
        progress = (completed / total) * 100
        self.progress['value'] = progress
        self.update_idletasks()  # Force an update of the GUI.

    def start_server(self):
        server_port = self.server_port_entry.get()
        if not server_port:
            self.status_label.config(text="Server port not provided.")
            return
        self.server = Server(port=int(server_port), gui=self)
        self.connect_button.config(state=tk.DISABLED)
        self.stop_server_button.config(state=tk.NORMAL)
        self.server_port_entry.config(state=tk.DISABLED)
        self.start_server_button.config(state=tk.DISABLED)
        self.ip_entry.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.DISABLED)
        Thread(target=self.server.start).start()

    def stop_server(self):
        self.connect_button.config(state=tk.NORMAL)
        self.stop_server_button.config(state=tk.DISABLED)
        self.server_port_entry.config(state=tk.NORMAL)
        self.start_server_button.config(state=tk.NORMAL)
        self.ip_entry.config(state=tk.NORMAL)
        self.port_entry.config(state=tk.NORMAL)
        if self.server:
            self.server.stop()

    def connect_to_server(self):
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        if not ip:
            self.status_label.config(text="IP address not provided.")
            return
        if not port:
            self.status_label.config(text="Port not provided.")
            return
        if self.client is None or not self.client.is_connected:
            self.client = Client(host=ip, port=int(port), save_dir=self.save_dir, gui=self)
            print(f'Client.gui: {self.client.gui}')  # Debug print
            connection_status = self.client.connect_to_server()

            if connection_status:
                self.status_label.config(text="Connected to server.")
                self.connect_button.config(text="Disconnect from Server")
                Thread(target=self.client.receive_file).start()  # Moved here
            else:
                self.status_label.config(text="Failed to connect to server.")
        else:
            self.client.disconnect_from_server()
            self.start_server_button.config(state=tk.NORMAL)
            self.status_label.config(text="Disconnected from server.")
            self.connect_button.config(text="Connect to Server")

    def select_save_dir(self):
        self.save_dir = filedialog.askdirectory()
        if self.save_dir:
            self.save_dir_label.config(text=f"Save Directory: {self.save_dir}")
            # Enable other widgets after selecting save directory
            self.ip_entry.config(state=tk.NORMAL)
            self.port_entry.config(state=tk.NORMAL)
            self.connect_button.config(state=tk.NORMAL)
        else:
            self.save_dir_label.config(text="Save Directory: Not selected")

if __name__ == "__main__":
    Application().mainloop()