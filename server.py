import os
import sys
import socket

data = {}

# Format as follows: name(str) : pos(list[x(str), y(str)])
# Example: "iLollek" : ["412", "938"]

def save_position(x, y, name):
    data[name] = [x, y]
    print(f'Saved Position for {name}: X: {x} - Y: {y}')

def send_position(name):
    try:
        conn.send(f'{name}#{data[name][0]}#{data[name][1]}'.encode())
        print(f'Sent Position for {name}: X: {data[name][0]} -  Y: {data[name][1]}')
    except KeyError:
        conn.send(f'{name}#NONE'.encode())
        print(f'Sent Position for {name} Failed: Not Saved!')

def send_all_playernames():
    ack_string = ""
    for playername in data.keys():
        ack_string = ack_string + f'{playername}#'
    conn.send(ack_string.encode())


host = "localhost"
port = 8888

s = socket.socket()

s.bind((host, port))

while True:
    s.listen(1)
    conn, addr = s.accept()
    request = conn.recv(2048).decode()
    if "REQ=" in request:
        if "REQ=GETPOS" in request:
            request = request.split("#")
            send_position(request[1])
        elif "REQ=SENDPOS" in request:
            request = request.split("#")
            save_position(request[1], request[2], request[3])
        elif "REQ=GETALLNAMES" in request:
            send_all_playernames()
    else:
        print(f'Unknown Request: {request}')
    conn.close()