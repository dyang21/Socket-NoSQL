import socket
import ssl
import threading

class Serv_Socket:
    
    def __init__(self, sock=None) -> socket:
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER = 'localhost'
        self.ADDR_INFO = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '[DISCONNECTED]'

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER) #custom context
        #self.context = ssl._create_unverified_context()
        
        self.context.load_cert_chain('cert.pem', 'key.pem')
        

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.sock.bind(self.ADDR_INFO)
        else:
            self.sock = sock

    def handle_client(self, conn_socket, addr_info):
        print(f"[NEW CONNECTION] {addr_info} connected.")
        connected = True
        while connected:
            first_msg_length = conn_socket.recv(self.HEADER).decode(self.FORMAT) #DECODE FROM BYTE TO UTF
            if first_msg_length: #check if message if valid
                first_msg_length = int(first_msg_length) ##number of bytes
                msg = conn_socket.recv(first_msg_length).decode(self.FORMAT)
                print(f"[{addr_info}]{msg}")
                if msg == self.DISCONNECT_MESSAGE:
                    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")
                    break
                conn_socket.send("Msg received".encode(self.FORMAT))
        conn_socket.close()
    def start(self):
        self.sock.listen() #opens port
        self.ssock = self.context.wrap_socket(self.sock, server_side=True)

        print(f"[LISTENING] Server is listening on {self.SERVER} at Port {self.PORT}.")
        while True:
            #listen to mutiple clients

            sconn_socket, addr_info = self.ssock.accept()

            new_thread = threading.Thread(target=self.handle_client, args=(sconn_socket, addr_info))
            new_thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        

server_socket = Serv_Socket()
server_socket.start()

print("[STARTING] server is starting...")

