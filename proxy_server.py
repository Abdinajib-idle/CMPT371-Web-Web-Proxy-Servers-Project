from socket import *
import os
from datetime import datetime

def handle_req():
    return
    ### Logic to serve client if the obj is there else get it from the server


def main():
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    server_port = 12345
    server_ip = 'localhost'

    proxy_socket.bind((server_ip, server_port))
    proxy_socket.listen(5)

    print("Proxy Server running on port: " + str(server_port))

    while True:
        clientConn, addr = proxy_socket.accept()
        handle_req(clientConn)



if __name__ == "__main__":
    main()