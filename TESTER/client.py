# client.py
import socket
import struct

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server {self.host}:{self.port}")

    def send_value(self, value):
        try:
            packed_data = struct.pack('!I', value)  # Pack the integer value as binary data
            self.client_socket.sendall(packed_data)
            print(f"Sent value to server: {value}")
        except struct.error as e:
            print(f"Error while packing data: {e}")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    client = Client('localhost', 8888)
    client.connect()
    value_to_send = 222222222222222222
    client.send_value(value_to_send)
