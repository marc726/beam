from tkinter import *

root = Tk()

#Basic Window Info
root.title("File Transfer")
root.minsize(290, 400)  # width, height

#Client
clientTitleText = Label(root, text="Client").grid(column=0,row=0,padx=10, pady=10)
clientIPLabel = Label(root, text="IP to Connect to:").grid(column=0,row=1,padx=10)
clientIPEntry = Entry(root).grid(column=0,row=2,padx=10)
clientPortLabel = Label (root, text="Port:").grid(column=0,row=3,padx=10, pady=10)
clientPortEntry = Entry(root).grid(column=0,row=4,padx=10, pady=10)
clientButtonConnect = Button(root, text="Connect").grid(column=0,row=5,padx=10)

#Server
serverTitleText = Label(root, text="Server").grid(column=1,row=0)
serverPortText = Label(root, text="Port to host on:").grid(column=1,row=1)
serverPortEntry = Entry(root).grid(column=1,row=2,padx=10)
serverStartStopButton = Button(root,text="Start Server").grid(column=1,row=3,padx=10)

root.mainloop() 