import socket

def read_message(socket : socket.socket):
    msg = ""
    while True:
        tmp = socket.recv(1024).decode()
        msg += tmp
        if len(tmp) < 1024:
            return msg


def send_message(sock : socket.socket, msg : str):
    total_length = len(msg)
    bytes_sent = 0
    while bytes_sent < total_length:
        bytes_sent += sock.send(msg[bytes_sent:bytes_sent + 1024].encode())