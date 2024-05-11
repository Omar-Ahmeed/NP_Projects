import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 7000))
server.listen()

clients = []
nicknames = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message)
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message, client)  # Pass sender's client socket to exclude from broadcast
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
        
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("Nickname".encode('utf-8'))
        nickname = client.recv(1024)
        
        nicknames.append(nickname)
        clients.append(client)
        
        broadcast(f"{nickname} connected to server".encode('utf-8'), client)  # Exclude sender from broadcast
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
        
receive()
