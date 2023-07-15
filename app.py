import tkinter as tk
from tkinter.filedialog import askdirectory
import socket


class Application(tk.Tk):
	def __init__(root):
		tk.Tk.__init__(root)

		root.title("File Transfer")
		root.minsize(300,300)
		root.maxsize(400,400)
		root.saveLocation = None

		#Server
		root.serverTitle = tk.Label(root, text="Server")
		root.serverTitle.grid(row=0,column=0,padx=10,pady=20)

		root.serverPortLabel = tk.Label(root,text="Host on Port:")
		root.serverPortLabel.grid(row=1,column=0,padx=10)

		root.serverPortEntry = tk.Entry(root)
		root.serverPortEntry.grid(row=2,column=0,padx=10)

		root.serverConnectButton = tk.Button(root,text="Start Server")
		root.serverConnectButton.grid(row=3,column=0,padx=10)

		root.space1 = tk.Label(root, text=" ").grid(row=4,column=0,pady=10)

		root.computerLocalIP = tk.Label(root, text=f"Your local IP is: \n{socket.gethostbyname(socket.gethostname())}")
		root.computerLocalIP.grid(row=5,column=0)

		root.space1 = tk.Label(root, text=" ").grid(row=6,column=0,pady=10)

		root.currentSaveLocation = tk.Label(root,text=f"Save Location:\n{root.saveLocation}")
		root.currentSaveLocation.grid(row=7,column=0,pady=10)

		root.selectSaveLocation = tk.Button(root,text="Select Save Location",command=root.saveSelect)
		root.selectSaveLocation.grid(row=8,column=0)

		#Client
		root.clientTitle = tk.Label(root, text="Client")
		root.clientTitle.grid(row=0,column=1,padx=10,pady=20)

		root.clientIPLabel = tk.Label(root, text="IP to Connect to:")
		root.clientIPLabel.grid(row=1,column=1,padx=10)

		root.clientIPEntry = tk.Entry(root)
		root.clientIPEntry.grid(row=2,column=1,padx=10,pady=10)

		root.clientPortLabel = tk.Label(root,text="Port to Connect to:")
		root.clientPortLabel.grid(row=3,column=1,padx=10)

		root.clientPortEntry = tk.Entry(root)
		root.clientPortEntry.grid(row=4,column=1,padx=10,pady=10)

		root.clientButtonConnect = tk.Button(root,text="Connect",state='disabled')
		root.clientButtonConnect.grid(row=5,column=1,padx=10)

		root.space1 = tk.Label(root, text=" ").grid(row=6,column=1,pady=10)

	def saveSelect(root):
		directory = askdirectory()
		if directory:  # directory will be '' if the user presses "Cancel"
			root.saveLocation = directory
			root.currentSaveLocation.config(text=f"Save Location: {root.saveLocation}")
			root.clientButtonConnect.config(state='normal')


if __name__ == "__main__":
	Application().mainloop()