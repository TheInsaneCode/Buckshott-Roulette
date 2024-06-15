import socket
import json

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.110', 5555))  # Connect to a server

# Function to send data (dictionary) to the server
def send_data(data):
    try:
        client.send(json.dumps(data).encode('utf-8'))
    except TypeError:
        print("Data is not serializable")

# Function to receive data (dictionary) from the server
def receive_data():
    try:
        data = client.recv(1024).decode('utf-8')
        return json.loads(data)  # Assuming data is in JSON format
    except json.JSONDecodeError:
        print("Received non-JSON data")
        return None

# Example usage
# send_data({'hi': 1000})
# send_data(input("Enter your name> "))

import tkinter as tk

# Create the main window
name = None
def retrieve_input(root):
    global name
    name = entry.get()
    root.destroy()
    
root = tk.Tk()
root.title("Enter Name")
root.geometry("300x100")
root.resizable(False, False)

# Create an entry field
entry = tk.Entry(root)
entry.pack()

enter_button = tk.Button(root, text="Enter", command=lambda: retrieve_input(root))
enter_button.pack()
root.mainloop()
send_data({'name':name})
while True:
    print(receive_data())
    pass

