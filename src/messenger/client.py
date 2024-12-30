import socket
import sys
import signal
import select
from . import PORT
from . import sockops

def client_main(hostname : str):
    parent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    parent_socket.connect((hostname, PORT))

    default_inputs = [parent_socket, sys.stdin]

    def graceful_close(sig, frame):
        parent_socket.close()
        exit()

    signal.signal(signal.SIGINT, graceful_close)

    send_msg = None
    while True:
        readable, _, _ = select.select(default_inputs, [], [])

        for read_sock in readable:
            if read_sock is parent_socket:
                recv_msg = sockops.read_message(read_sock)
                if recv_msg == "":
                    # Nothing recieved from a readable socket == closed conn
                    read_sock.close()
                    print("SERVER CLOSED -- terminating")
                    exit()
                else:
                    sys.stdout.write(f"> {recv_msg}")
                    sys.stdout.flush()
            elif read_sock is sys.stdin:
                send_msg = sys.stdin.readline()
                sockops.send_message(parent_socket, send_msg)