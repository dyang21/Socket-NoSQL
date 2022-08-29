import socket
import ssl


class client_Socket:
    def __init__(self, sock=None) -> socket:
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER = 'localhost'
        self.ADDR_INFO = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = '[DISCONNECTED]'
        #self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

        self.context = ssl._create_unverified_context()
        self.context.load_verify_locations('localhost.pem')

        #self.context.load_cert_chain(certfile="localhost.crt", keyfile="./private.key")

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

'''
    def send(self,msg) -> None:
        message = msg.encode(self.FORMAT) #bytes
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length)) #byte representation
        self.sock.send(send_length)
        self.sock.send(message)
'''

client_sock = client_Socket()
with client_sock.sock as sock:
    s_client = client_sock.context.wrap_socket(sock, server_hostname='localhost')
    s_client.connect(client_sock.ADDR_INFO)
    print('connection established')


##_client.send('Hello Server - From Client')
'''
msg = 'Hello Server - From Client'
message = msg.encode(client_sock.FORMAT)
msg_length = len(message)
send_length = str(msg_length).encode(client_sock.FORMAT)
send_length += b' ' * (client_sock.HEADER - len(send_length))
s_client.send(send_length)
s_client.send(message)
'''



input()

s_client.send('[DISCONNECTED]')


