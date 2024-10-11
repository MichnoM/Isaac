import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.12"
        self.port = 5555
        self.address = (self.server, self.port)
        self.info = self.connect()

    def getP(self):
        return self.info[1]
    
    def getMap(self):
        return self.info[0]
    
    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048*10))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*10))
        except socket.error as e:
            print(e)