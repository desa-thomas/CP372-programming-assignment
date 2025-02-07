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
        
        self.active_clients = 0
        self.lock = threading.Lock()
    
    def handle_client(self, client_socket: socket.socket, address, i):
        """
        Function to handle client i
        """
        
        with self.lock:
            self.active_clients += 1
    
        #First message sent from client is name
        name = client_socket.recv(1024).decode()
        if name:
            print(f"Client{i}: {name} connected")
            print(f"{self.active_clients} active clients")

            client_socket.send(bytes(f"Welcome {name}: Enter any string, or 'status' to see client information", 'utf-8'))
            
            #Store client info
            self.client_name_dict[f"Client{i}"] = []
            self.client_name_dict[f"Client{i}"].append(name)
            self.client_name_dict[f"Client{i}"].append(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            self.client_name_dict[f"Client{i}"].append("Active")

        
        #Maintain connection and echo {data} ACK while they are connected
        while True:
            
            data = client_socket.recv(1024).decode()
            
            #If client closes connection
            if not data:
                break
            
            #Send status if requested
            if(data.lower() == "status" ):
                status = "\n" + "-"*75 + "\n"
                status += f"{"Client id":<12}{"Name":<15}{"Start time":<24}{"End time":<24}"
                status += "\n\n"
                
                #iterate ovfer dict
                for client in self.client_name_dict.items():
                    status += f"{client[0]:<12}"
                    #iterate over info array
                    for x in range(len(client[1])):
                        if x == 0:
                             status += f"{client[1][x]:<15}"
                        else: 
                            status += f"{client[1][x]:<24}"
                    
                    status += "\n"
                    
                status += "-"*75 + "\n"
                
                client_socket.send(bytes(status, "utf-8"))
            else: 
                #Echo message back with ACK
                client_socket.send(bytes(f"{data} ACK", "utf-8"))
                
        #store end time
        self.client_name_dict[f"Client{i}"][2]= (datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        print(f"{name} quit: {address}")
        client_socket.close()
        
        with self.lock:
            self.active_clients -= 1


    def start_server(self):
        """
        Function to start the server
        """
        self.server_socket.listen(server.MAX_CLIENTS)
        print("Server is listening...")
        
        while True:
            #Reject connections when there are move than MAX_CLIENTS active clients
                
            client_socket, addr = self.server_socket.accept()
            full = False
            
            with self.lock:
                #If server full, reject connection
                if self.active_clients == server.MAX_CLIENTS:
                    print("server full")
                    full = True
                    client_socket.send(bytes("Server is full. Try again later.", "utf-8"))
                    client_socket.close()
                    pass
                else: 
                    client_socket.send(bytes("OK", "utf-8"))
            
            if not full:
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

