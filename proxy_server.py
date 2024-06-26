from socket import *
import os
from datetime import datetime

def handle_req():
    return
    ### Logic to serve client if the obj is there else get it from the server


def main():
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_host = 12345
    proxy_server_host = 'localhost'


    server_host = 8080

    server_ip = 'localhost'

    proxy_socket.bind((server_ip, proxy_host))
    proxy_socket.listen(5)

    print("Proxy Server running on port: " + str(proxy_host))

    while True:
        clientConn, addr = proxy_socket.accept()
        print("conn received from {addr}")
        handle_req(clientConn)



if __name__ == "__main__":
    main()