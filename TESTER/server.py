# server.py
import socket
import struct

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        self.accept_connections()

    def accept_connections(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            print("Accepted connection from client")
            self.handle_client(client_socket)

    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(4)  # Receive 4 bytes (32 bits) of data
            if not data:
                return
            value = struct.unpack('!I', data)[0]  # Unpack the binary data as an unsigned integer
            print(f"Received value from client: {value}")
        except struct.error as e:
            print(f"Error while unpacking data: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = Server('localhost', 8888)
    server.start()
