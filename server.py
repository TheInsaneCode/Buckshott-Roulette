import socket
import threading
import json
from msvcrt import getch
from random import randint

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.0.110', 5555))  # Bind to an address and port
server.listen()

clients = []
addresses = {}
names = []

game_state = {
    'd_count': 3,
    'health_total': 4,
    'turn': randint(1,2),
    'ended': False,
    'lost': False,
    'level': 1,
    'dead': False
}

     
def broadcast(data):
    for client in clients:
        send_to_client(client, data)

# Modified handle_client function
def handle_client(client):
    global names  # Use the global game_state variable
    while True:
        try:
            data = json.loads(client.recv(1024).decode('utf-8'))
            if data:
                print(f"Received data: {data}")
                if 'turn' in data:
                    game_state = data
                    broadcast(game_state)  # Broadcast updated game state
                if 'name' in data:
                    names.append(data['name'])
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break

# Function to send initial True message and game state
def send_initial_data():
    for client in clients:
        send_to_client(client, True)  # Send True to both clients
        send_to_client(client, game_state)  # Send initial game state

# Function to send data to a specific client
def send_to_client(client, data):
    try:
        client.send(json.dumps(data).encode('utf-8'))
    except TypeError:
        print("Data is not serializable")

# Main function to receive clients and handle keyboard inputs

        
def receive():
    while True:...
                

print("Server is running...")
print("Waiting for clients to connect...")
# detected = False
# while len(clients)< 2:
#     client, address = server.accept()
#     print(f"Connected with {str(address)}")

#     clients.append(client)
#     addresses[client] = address

#     # Start handling thread for client
#     thread = threading.Thread(target=handle_client, args=(client,))
#     thread.start()
#     if len(clients) == 1 and not detected:
#         detected = True
#         print("player connected 1/2")
# else:
#     print("player connected 2/2 ...")    
while len(clients) < 2:
    client, address = server.accept()
    print(f"Connected with {str(address)}")

    clients.append(client)
    addresses[client] = address

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()
else:
    while len(names) < 2:
        continue
    if len(clients) == 2 and len(names) == 2:  # Check if two players have connected
        print("Both players connected...")
        print(names[0],'vs', names[1])
        send_initial_data()  # Send initial data to both clients

# ... [rest of your server class code] ..
    
# Start handling thread for client

# client, address = server.accept()
# clients.append(client)
# addresses[client] = address
# thread = threading.Thread(target=handle_client, args=(client,))

# thread.start()



receive()