from lzma import FORMAT_ALONE
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

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        
        self.context.load_verify_locations('cert.pem') #self signed ssl


        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock




client_sock = client_Socket()
with client_sock.sock as sock:
    s_client = client_sock.context.wrap_socket(sock, server_hostname='localhost')
    s_client.connect(client_sock.ADDR_INFO)
    print('connection established')


##_client.send('Hello Server - From Client')

def send(s_client,msg) -> None:
    message = msg.encode(client_sock.FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(client_sock.FORMAT)
    send_length += b' ' * (client_sock.HEADER - len(send_length))
    s_client.send(send_length)
    s_client.send(message)


send(s_client,"Hello world")

input()
send(s_client,"[DISCONNECTED]")



