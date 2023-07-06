import tkinter as tk
from tkinter import filedialog
from threading import Thread
from client import Client
from server import Server

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

        # other widgets...

        self.client = None
        self.server = None
        self.save_dir = None

    def start_server(self):
        if not self.save_dir:
            self.status_label.config(text="Save directory not selected.")
            return
        server_port = self.server_port_entry.get()
        if not server_port:
            self.status_label.config(text="Server port not provided.")
            return
        self.server = Server(save_dir=self.save_dir, port=int(server_port))
        server_port = int(self.server_port_entry.get())
        if not server_port:
            self.status_label.config(text="Server port not provided.")
            return
        self.server = Server(port=server_port)
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
        port = int(self.port_entry.get())
        if not ip:
            self.status_label.config(text="IP address not provided.")
            return
        if not port:
            self.status_label.config(text="Port not provided.")
            return
        if self.client is None or not self.client.is_connected:
            self.client = Client(host=ip, port=int(port))
            connection_status = self.client.connect_to_server()
            self.start_server_button.config(state=tk.DISABLED)

            if connection_status:
                self.status_label.config(text="Connected to server.")
                self.connect_button.config(text="Disconnect from Server")
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
        else:
            self.save_dir_label.config(text="Save Directory: Not selected")

if __name__ == "__main__":
    Application().mainloop()