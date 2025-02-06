import threading
import socket
from datetime import datetime

class server:
    MAX_CLIENTS = 3
    
    def __init__(self):
        #initialize server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 1738))
        
        #Client name dictionary {'Client - #' : [name, start time, end time]}
        self.client_name_dict = {}
        self.count = 1
    
    def handle_client(self, client_socket: socket.socket, address, i):
        """
        Function to handle client i
        """
        print(f"{address} connected @: {datetime.now()}")
        
        #First message sent from client is name
        name = client_socket.recv(1024).decode()
        if name:
            print(f"Client{i} - {name}")
            client_socket.send(bytes(f"Welcome {name}", 'utf-8'))
            
            #Store clients name
            self.client_name_dict[f"Client{i}"].insert(0, name) 
        
        #Maintain connection and echo {data} ACK while they are connected
        while True:
            
            data = client_socket.recv(1024).decode()
            #If client closes connection
            if not data:
                break
            
            #Echo message back with ACK
            client_socket.send(bytes(f"{data} ACK", "utf-8"))
            
        #store end time
        self.client_name_dict[f"Client{i}"].append(datetime.now().timestamp())
        print(f"Connection closed: {address}")
        print(f"Client{i} : {self.client_name_dict[f"Client{i}"]}")
        client_socket.close()

    def start_server(self):
        self.server_socket.listen(server.MAX_CLIENTS)
        print("Server is listening")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            #i = client #
            i = self.count
            self.count += 1 
            self.client_name_dict[f"Client{i}"] = [datetime.now().timestamp()]
            
            #create thread to handle client # i
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr, i))
            client_thread.daemon = True
            client_thread.start()
            
        return


if __name__ == '__main__':
    Server = server()
    Server.start_server()

