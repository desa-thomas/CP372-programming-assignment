import threading
import socket
from datetime import datetime
import os 

class server:
    """
    Server class
    
    attributes:
        self.count            : (int)    number of clients that have connected (since server start)
        self.client_name_dict : (dict)   dictionary containing information about connected clients
        self.server_socket    : (socket) server socket
        self.active_clients   : (int)    Number of currently active clients on server
        self.lock             : (Lock)   Thread lock for threads 
    """
    MAX_CLIENTS = 3
    
    def __init__(self):
        
        #initialize server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 1738))
        
        #Client name dictionary {'Client - #' : [name, start time, end time]}
        self.client_name_dict = {}
        self.count = 1
        
        #Thread lock for changing active clients on each thread
        self.active_clients = 0
        self.lock = threading.Lock()
    
    def handle_client(self, client_socket: socket.socket, address, i):
        """
        Function to handle client i's session. Called by thread i
        """
        
        with self.lock:
            self.active_clients += 1
    
        #First message sent from client is name
        name = client_socket.recv(1024).decode()
        if name:
            print(f"Client{i}: {name} connected")
            
            s = f"Welcome {name}. Enter any string, or 'status' to see server cache"
            welcome_msg = f"{"*"*5}  {s}  {"*"*5}" 
            client_socket.send(bytes(f"\n{welcome_msg:>100}", 'utf-8'))
            
            #Store client info
            self.client_name_dict[f"Client{i}"] = []
            self.client_name_dict[f"Client{i}"].append(name)
            self.client_name_dict[f"Client{i}"].append(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            self.client_name_dict[f"Client{i}"].append("Active") #update this once Client socket is closed

        #If user closes connection before providing name
        else:
            with self.lock: 
                self.active_clients -= 1  
            return
        #Maintain connection and echo {data} ACK while they are connected (or status)
        while True:
            
            data = client_socket.recv(1024).decode()
            
            #If client closes connection
            if not data:
                break
            
            #Send status if requested
            if(data.lower() == "status" ):
                status = "|\n|" + "-"*75 + "\n"
                status += f"| {"Client id":<12}{"Name":<15}{"Start time":<24}{"End time":<24}"
                status += "\n|\n"
                
                #iterate over client_name_dict
                for client in self.client_name_dict.items():
                    status += f"| {client[0]:<12}"
                    
                    #iterate over info array => [name, start, end]
                    for x in range(len(client[1])):
                        if x == 0:
                             status += f"{client[1][x]:<15}"
                        else: 
                            status += f"{client[1][x]:<24}"
                    
                    status += "\n"
                status += "|" + "-"*75
                
                client_socket.send(bytes(status, "utf-8"))
            
            #If client requests server file list
            elif(data.lower() == "list"): 
                list_str = "|"
                for file in os.listdir("server-files"):
                    list_str += f"\n| {file}"
                
                client_socket.send(bytes(list_str, "utf-8"))
                #receive clients requested file
                requested_file = client_socket.recv(1024).decode()
                
                if requested_file:
                    
                    while requested_file not in os.listdir("server-files"):
                        #Stop searching for file
                        if requested_file == "<":
                            break
                        client_socket.send(bytes(f"|\n| ERROR: file not found, try again (< to stop selecting file)\n{list_str}", "utf-8"))
                        requested_file = client_socket.recv(1024).decode()
                    
                    #If file exists send it to client
                    if requested_file != "<":
                        with open(f"server-files/{requested_file}", "rb") as file:
                            client_socket.sendfile(file)
                    else:
                        print(" here ")
                        #if client hit "<" send '\n' so both client and server aren't stuck listening
                        client_socket.send(bytes("pass", "utf-8"))
                        
                #if nothing is recieved client disconnected
                else:
                    with self.lock:
                        self.active_clients -=1
                    break
                    
            else: 
                #Echo message back with ACK
                client_socket.send(bytes(f"|\n| {data} ACK", "utf-8"))
                
        #Connection is closed -> store end time
        self.client_name_dict[f"Client{i}"][2]= (datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        print(f"{name} quit: {address}")
        client_socket.close()
        
        #Decrement active clients
        with self.lock:
            self.active_clients -= 1


    def start_server(self):
        """
        Function to start the server
        """
        self.server_socket.listen(server.MAX_CLIENTS)
        print("Server is listening...")
        
        while True:                
            client_socket, addr = self.server_socket.accept()
            full = False
            
            #Check active connections
            #if > max_clients, send message that server is full and close socket
            with self.lock:
                if self.active_clients == server.MAX_CLIENTS:
                    full = True
                    print(f"server full - {addr} rejected")
                    client_socket.send(bytes("Server is full", "utf-8"))
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

