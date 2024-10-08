from socket import *
import os
from datetime import datetime

def process_req(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8').split('\r\n')
        request_line = request[0].split()
        print('\n')
        for line in request:
            print(line)

        if len(request_line) < 3:
            response = 'HTTP/1.1 400 Bad Request\r\n\r\nBad Request'
            client_socket.sendall(response.encode())
            client_socket.close()
            return

        method, path, _ = request_line

        if method not in ['GET', 'HEAD']:
            response = 'HTTP/1.1 400 Bad Request\r\n\r\nOnly GET and HEAD methods are supported.'
            client_socket.sendall(response.encode())
            client_socket.close()
            return
        
        if path == '/':
            path = '/test.html'
        
        file_path = path[1:]  # Remove leading '/'

        if not os.path.isfile(file_path):
            response = 'HTTP/1.1 404 Not Found\r\n\r\nFile Not Found'
        elif not os.access(file_path, os.R_OK):
            response = 'HTTP/1.1 403 Forbidden\r\n\r\nAccess Denied'
        else:
            last_modified = os.path.getmtime(file_path)
            last_modified_date = datetime.utcfromtimestamp(last_modified).strftime('%a, %d %b %Y %H:%M:%S GMT')

            if_modified_since = None
            for header in request:
                if header.startswith('If-Modified-Since:'):
                    if_modified_since = header.split(' ', 1)[1]
                    break

            if if_modified_since:
                 if_modified_since_date = datetime.strptime(if_modified_since, '%a, %d %b %Y %H:%M:%S GMT')
                 if if_modified_since_date >= datetime.strptime(last_modified_date, '%a, %d %b %Y %H:%M:%S GMT'):
                    response = 'HTTP/1.1 304 Not Modified\n'
                    client_socket.sendall(response.encode())
                    client_socket.close()
                    return
            
            with open(file_path, 'r') as file:
                content = file.read()
            response = f'HTTP/1.1 200 OK\r\nLast-Modified: {last_modified_date}\r\n\r\n{content}'
        
        client_socket.sendall(response.encode())
    except Exception as e:
        response = f'HTTP/1.1 400 Bad Request\n\n{str(e)}'
        client_socket.sendall(response.encode())
    finally:
        client_socket.close()

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_port = 8080
    server_ip = 'localhost'

    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)

    print("Server running on port: " + str(server_port))

    while True:
        clientConn, addr = server_socket.accept()
        process_req(clientConn)



if __name__ == "__main__":
    main()