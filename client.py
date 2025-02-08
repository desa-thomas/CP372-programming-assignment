import socket
import os

def start_client():
    #clear CLI screen
    size = os.get_terminal_size().columns
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{"CP372 Programming Assignment Client Interface":-^{size}}")
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1738))  # Connect to the server
    
    # Check if the server rejected the connection
    init_message = client_socket.recv(1024).decode()
    if init_message != "OK":
        print(f"\n{"Server full ... Connection rejected"}\n")
        client_socket.close()
        return  

    #First message cilent sends name
    print("(quit/q to exit)")
    print("\nEnter name:\n|", end="")


    # if message.lower() == "quit" or message.lower() == "q":
    #     client_socket.close()
    #     return
    # client_socket.send(message.encode())
    # data = client_socket.recv(1024).decode()
    # print(f"{data}\n")

    
    #Main loop, clien can send any string
    while True:
        message = input("\n|--> ")
        if message.lower() == "quit" or message.lower() == "q":
            break
        
        #don't allow empty strings
        elif message == "":
            continue
        
        client_socket.send(message.encode())

        data = client_socket.recv(1024).decode()
        
        if(data != "pass"): 
            print(f"{data}")    

    client_socket.close()

if __name__ == '__main__':
    start_client()
