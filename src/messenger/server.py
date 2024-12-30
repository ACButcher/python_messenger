import socket
import sys
import signal
import select
from . import PORT
from . import sockops

def server_main():
    parent_socket = socket.socket(
        family = socket.AF_INET, 
        type = socket.SOCK_STREAM,
    )
    parent_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    parent_socket.bind(("", PORT)) # Assigns name to parent socket
    parent_socket.listen(10)

    default_inputs = [parent_socket, sys.stdin]
    clients = []

    def graceful_close(sig, frame):
        for client in clients:
            client.close()
        parent_socket.close()
        exit()

    signal.signal(signal.SIGINT, graceful_close)

    while True:
        #TODO: Refactor to use select.poll
        readable, _, _ = select.select(default_inputs + clients, [], [])

        for read_sock in readable:
            if read_sock is parent_socket:
                # Handle new connection
                client_socket, _ = parent_socket.accept()
                clients.append(client_socket)
            elif read_sock is sys.stdin:
                # Sending a message
                send_msg = sys.stdin.readline()
                sockops.send_message(clients[0], send_msg)
            else:
                # Receiving a message
                recv_msg = sockops.read_message(read_sock)
                if recv_msg == "":
                    # Close the connection
                    clients.remove(read_sock)
                    read_sock.close()
                    print("<Client disconnected>")
                else:
                    sys.stdout.write(f"> {recv_msg}")
                    sys.stdout.flush()