import socket
from _thread import *
from src.player import Player
from src.map import Map
import pickle
from settings import window_width, window_height

server = "192.168.1.12"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Waiting for a connection, Server Started")

map = Map(window_width, window_height)
players = [Player(window_width//2, window_height//2), Player(window_width//2 + 200, window_height//2)]

def threaded_client(connection, player):
    global map
    connection.send(pickle.dumps((map, players[player])))
    reply = ""
    while True:
        try:
            data = pickle.loads(connection.recv(2048*10))
            map, players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = map, players[0]
                else:
                    reply = map, players[1]

                print("Received: ", data)
                print("Sending: ", reply)

            connection.sendall(pickle.dumps(reply))
        except:
            break
    
    print("Lost Connection")
    connection.close()

current_player = 0
while True:
    connection, address = s.accept()
    print("Connected to: ", address)

    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1