import socket
import os

def start_client():
    #clear CLI screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{"CP372 Programming Assignment Client Interface":-^100}")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1738))  # Connect to the server

    #First message cilent sends name
    message = input("\n(Enter name)--> ")
    client_socket.send(message.encode())
    data = client_socket.recv(1024).decode()
    print(f"{data}\n")

    
    #Main loop, clien can send any string
    while True:
        message = input("--> ")
        if message.lower() == "quit" or message.lower() == "q":
            break
        
        client_socket.send(message.encode())

        data = client_socket.recv(1024).decode()
        print(f"{data}\n")

    client_socket.close()

if __name__ == '__main__':
    start_client()
