import socket
from _thread import *
import random

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

boxes = []  # Lista boxów

def generate_boxes():
    global boxes
    for _ in range(10):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        boxes.append((x, y, 20))

if len(boxes) == 0:
    generate_boxes()

currentId = "0"
pos = ["0:50,50,1,0,0,0,100|", "1:100,100,1,0,0,0,100|"]


def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print("Client disconnected")
                conn.send(str.encode("Goodbye"))
                break
            else:
                reply = data.decode('utf-8')
                print("Received: " + reply)
                arr = reply.split(":")
                id = int(arr[0])

                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]

                boxes_reply = ""
                for box in boxes:
                    boxes_reply += f"{box[0]},{box[1]},{box[2]};"


                if "#" not in reply:
                    reply += "#" + boxes_reply

                print(f"Sending: {len(boxes)} boxes, {reply}")

                conn.sendall(str.encode(reply))
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    print("Connection Closed")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
