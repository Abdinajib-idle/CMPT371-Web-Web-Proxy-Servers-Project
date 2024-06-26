from socket import *
import os
from datetime import datetime
import threading

def handle_req(client_socket, server_host, server_port):
    try:
        #recv the req from client
        req = client_socket.recv(1024)

        #create server socket to connect target to server
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.connect((server_host, server_port))

        #forward req to the server
        server_socket.sendall(req)
    
    ### Logic to serve client if the obj is there else get it from the server


def main():
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_host = 12345
    proxy_server_host = 'localhost'


    server_port = 8080

    server_host = 'localhost'

    proxy_socket.bind((proxy_server_host, proxy_host))
    proxy_socket.listen(5)

    print("Proxy Server running on port: " + str(proxy_host))

    while True:
        client_socket, addr = proxy_socket.accept()
        print("conn received from {addr}")

        # new thread to handle client request
        proxy_thread = threading.Thread(target = handle_req, args = (client_socket, server_host, server_port))

        #starting thread
        proxy_thread.start()



if __name__ == "__main__":
    main()