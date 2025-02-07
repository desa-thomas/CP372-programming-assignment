import threading
import socket
from datetime import datetime

class server:
    """
    Server class
    
    attributes:
        self.count : (int) number of clients that have connected (since server start)
        self.client_name_dict : (dict) dictionary containing information about connected clients
        self.server_socket : (socket) server socket
    """
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
        #First message sent from client is name
        name = client_socket.recv(1024).decode()
        if name:
            print(f"Client{i}: {name} connected")
            client_socket.send(bytes(f"Welcome {name}", 'utf-8'))
            
            #Store client info
            self.client_name_dict[f"Client{i}"] = []
            self.client_name_dict[f"Client{i}"].append(name)
            self.client_name_dict[f"Client{i}"].append(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

        
        #Maintain connection and echo {data} ACK while they are connected
        while True:
            
            data = client_socket.recv(1024).decode()
            
            #If client closes connection
            if not data:
                break
            
            #Send status if requested
            if(data.lower() == "status" ):
                status = "\n" + "-"*100 + "\n"
                status += f"{"Client id":<10}{"Name":^30}{"Start time":^30}{"End time":^30}"
                status += "\n\n"
                
                #iterate ovfer dict
                for client in self.client_name_dict.items():
                    status += f"{client[0]:<10}"
                    #iterate over info array
                    for clientinfo in client[1]:
                        status += f"{clientinfo:^30}"
                    
                    status += "\n"
                    
                status += "-"*100 + "\n"
                
                client_socket.send(bytes(status, "utf-8"))
            else: 
                #Echo message back with ACK
                client_socket.send(bytes(f"{data} ACK", "utf-8"))
                
        #store end time
        self.client_name_dict[f"Client{i}"].append(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        print(f"{name} quit: {address}")
        client_socket.close()


    def start_server(self):
        """
        Function to start the server
        """
        self.server_socket.listen(server.MAX_CLIENTS)
        print("Server is listening")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            #i = client #
            i = self.count
            self.count += 1             
            #create thread to handle client # i
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr, i))
            client_thread.daemon = True
            client_thread.start()
            
        return


if __name__ == '__main__':
    Server = server()
    Server.start_server()

