from socket import *
import threading

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
        
        # Check if the response is in the cache
        if path in cache:
            print("Yay! Cache hit --> Serving from cache.")
            client_socket.sendall(cache[path])
        else:
            print("Cache miss --> Forwarding request to the server.")
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

            # Store the response in the cache
            cache[path] = response

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
