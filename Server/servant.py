import socket
import threading #Allowing for clients not to be waiting for other code

PORT = 5000 #Port thats not being used
SERVER = socket.gethostbyname(socket.gethostname()) #This will get the IP address of local network
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
BUFFER_SIZE = 1024


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a new socket for IPv4 and streaming information 
server.bind(ADDR) #The address has to be saved as a tuple for port and address

def handle_client(conn, addr):
    print(f"[NEW CONNECTION {addr} connected")
    connected = True
    confirmation = conn.recv(BUFFER_SIZE).decode(FORMAT)
    if(confirmation.strip() == DISCONNECT_MESSAGE):
        print("[DISCONNECTING CLIENT]")
    else:
        print(f"[TRANSACTION WITH {addr}] File transfer initiated")
        header = conn.recv(BUFFER_SIZE).decode(FORMAT)
        filename = header.strip()
        download = open(filename, 'wb')
        while connected:
            data = conn.recv(BUFFER_SIZE)
            if len(data) > 0:
                download.write(data)
            else:
                break
        download.close()
        print(f"[TRANSACTION WITH {addr}] Download complete")
        print("[DISCONNECTING CLIENT]")
    #connection with client is closed
    conn.close()


#This handles new connections
def start():
    server.listen()
    print(f"[Listening] Server is running on {SERVER}")
    while True:
        conn , addr = server.accept() #This will wait until a new connection comes in and then stores it in connection socket variable as well as its address
        thread = threading.Thread(target=handle_client, args = (conn, addr)) #when a new connection occurs will creat a new thread with target function and (conn, addr) as args
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") #shows how many threads there are

print("[STARTING] server is starting...")
start()