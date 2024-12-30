import argparse
from . import client, server

def main():
    parser = argparse.ArgumentParser(
        prog = "messenger",
        description = "A chat program using a client/server model"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", 
        "--server",
        action = "store_true",
        help = "Starts messenger as server"
    )
    group.add_argument(
        "-c",
        "--client",
        metavar="HOSTNAME",
        help = "Starts messenger as client and connects to HOSTNAME"
    )

    args_namespace = parser.parse_args()

    if args_namespace.client != None:
        client.client_main(args_namespace.client)
    elif args_namespace.server:
        server.server_main()
    else:
        print("Invalid usage -- run with -h flag")

if __name__ == "__main__":
    main()