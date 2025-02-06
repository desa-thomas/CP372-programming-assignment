import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1738))  # Connect to the server

    while True:
        message = input("Enter name: ")
        if message == "quit" or message == "q":
            break
        
        client_socket.send(message.encode())

        data = client_socket.recv(1024).decode()
        print(f"Received from server: {data}")

    client_socket.close()

if __name__ == '__main__':
    start_client()
