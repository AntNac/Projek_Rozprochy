import socket
from _thread import *
import random
import math
from box import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = 'localhost'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

boxes = []
players_level = [1, 1]

def generate_boxes():
    global boxes
    for i in range(10):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        boxes.append(Box(i, x, y,20))

if len(boxes) == 0:
    generate_boxes()

currentId = "0"
pos = ["0:50,50,1,0,0,0,100||", "1:100,100,1,0,0,0,100||"]

def threaded_client(conn, player_id):
    global currentId, pos, boxes
    conn.send(str.encode(currentId))
    currentId = "1"

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                print("Client disconnected")
                break

            reply = data.decode('utf-8')
            arr = reply.split(":")
            id = int(arr[0])

            pos[id] = reply

            if id == 0: nid = 1
            if id == 1: nid = 0

            main_data, boxes_data = reply.split("#")
            player_info, bullet_info, hitbox_info = main_data.split("|")
            if hitbox_info:
                for box_id_str in hitbox_info.split(";"):
                    if box_id_str:
                        box_id = int(box_id_str)
                        for box in boxes:
                            if box.id == box_id and box.hp > 0:
                                destroyed = box.get_hit(5)
                                if destroyed:
                                    players_level[id] += 1
                                break

            boxes = [box for box in boxes if box.hp > 0]

            other_player_data = pos[nid].split("#")[0]
            new_reply = other_player_data + "#"
            for box in boxes:
                new_reply += f"{box.id},{box.x},{box.y},{box.hp};"

            print(f"Sending: {len(boxes)} boxes")
            conn.sendall(str.encode(new_reply))
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, int(currentId)))
