from socket import *
import threading
from datetime import datetime
import os
# Cache to store responses
cache = {}

def handle_req(client_socket, server_host, server_port):
    try:
        # Receive the request from the client
        req = client_socket.recv(1024).decode('utf-8')
        print(f"Request received from client:\n{req}")

        # Modify the request to remove the hostname
        request_lines = req.split('\r\n')
        request_line = request_lines[0].split()
        if len(request_line) > 1:
            path = request_line[1]
            if path.startswith('http://'):
                path = path[path.find('/', 7):]  # Remove http://hostname
            request_lines[0] = f"{request_line[0]} {path} {request_line[2]}"
        modified_request = '\r\n'.join(request_lines).encode('utf-8')
        
        # Extract the If-Modified-Since header if present
        if_modified_since = None
        for header in request_lines:
            if header.startswith('If-Modified-Since:'):
                if_modified_since = header.split(' ', 1)[1]
                break
        
        # Check if the response is in the cache
        if path in cache:
            cached_response, last_modified = cache[path]
            if if_modified_since:
                if_modified_since_date = datetime.strptime(if_modified_since, '%a, %d %b %Y %H:%M:%S GMT')
                last_modified_date = datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S GMT')
                if if_modified_since_date >= last_modified_date:
                    print("Cache hit with same modification time. Returning 304 Not Modified.")
                    response = 'HTTP/1.1 304 Not Modified\r\n\r\n'
                    client_socket.sendall(response.encode())
                    client_socket.close()
                    return
            print("Cache hit. Serving from cache.")
            client_socket.sendall(cached_response)
        else:
            print("Cache miss. Forwarding request to the server.")
            # Create server socket to connect to the target server
            server_socket = socket(AF_INET, SOCK_STREAM)
            server_socket.connect((server_host, server_port))

            # Forward the modified request to the server
            server_socket.sendall(modified_request)

            response = b""
            while True:
                # Receive the response from the server
                res = server_socket.recv(4096)
                if len(res) > 0:
                    response += res
                else:
                    break

            # Extract Last-Modified header from server response
            response_lines = response.decode('utf-8').split('\r\n')
            last_modified = None
            for header in response_lines:
                if header.startswith('Last-Modified:'):
                    last_modified = header.split(' ', 1)[1]
                    break
            
            if last_modified:
                # Store the response and last modified date in the cache
                cache[path] = (response, last_modified)
            
            # Forward the response to the client
            client_socket.sendall(response)

            # Termination of sockets
            server_socket.close()
        client_socket.close()
    except Exception as e:
        print(f"Proxy request error: {e}")
        client_socket.close()

def main():
    proxy_socket = socket(AF_INET, SOCK_STREAM)
    proxy_host = 'localhost'
    proxy_port = 12345

    server_host = 'localhost'
    server_port = 8080

    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)

    print("Proxy Server running on port: " + str(proxy_port))

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"Connection received from {addr}")

        # New thread to handle client request
        proxy_thread = threading.Thread(target=handle_req, args=(client_socket, server_host, server_port))

        # Start the thread
        proxy_thread.start()

if __name__ == "__main__":
    main()
