# Uncomment this to pass the first stage
import socket
import threading
import os
import sys

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    while True:
        (conn, address) = server_socket.accept() # wait for client
        t =threading.Thread(target=lambda: request_handler(conn))
        t.start()
    
    
def request_handler(conn: socket.socket):
        val = conn.recv(1024)
        pars = val.decode()
        args = pars.split("\r\n")
        
        # Split the request line and extract http info
        request_line = args[0].split(" ")
        http_method = request_line[0]
        request_target = request_line[1]
        http_version = request_line[2]
        
        # Split the headers line
        header_host = args[1]
        user_agent = args[2]
        media_type = args[3]
        body = args[4]
        
        print(f"http method: {http_method}")
        print(f"request target: {request_target}")
        print(f"http version: {http_version}")
        
        print(f"Host: {header_host}")
        print(f"Agent: {user_agent}")
        print(f"Type: {media_type}")
        print(f"Body: {body}")
            
            
        # Default responses
        response_200 = b"HTTP/1.1 200 OK\r\n\r\n"
        response_404 = b"HTTP/1.1 404 Not Found\r\n\r\n"
        
        # Custom responses
        response_201 = f"HTTP/1.1 201 Created\r\n\r\n".encode()
        
        response = response_404
        if len(args) > 1:
            path = args[0].split(" ")
            if request_target == "/":
                response = response_200
            elif request_target.startswith("/echo/"):
                string = request_target.replace("/echo/", "")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            if "user" in path[1]:
                path = args[2]
                string = path.replace("User-Agent: ", "")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            if "files" in path[1]:
                if "POST" in path[0]:
                    directory = sys.argv[2]
                    try:
                        os.mkdir(directory)
                    except FileExistsError as e:
                        print(f"Directory {directory} already exist")
                    file = path[1].replace("/files/", "")
                    body = args[-1]
                    with open(os.path.join(directory, file), "w") as f:
                        f.write(body)
                    response = f"HTTP/1.1 201 Created\r\n\r\n".encode()
                else:
                    directory = sys.argv[2]
                    file = path[1].replace("/files/", "")
                    if os.path.isfile(f"/{directory}/{file}"):
                        with open(f"/{directory}/{file}", "r") as f:
                            lines = ""
                            for word in f:
                                lines += word
                            lines_len = len(lines)
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {lines_len}\r\n\r\n{lines}".encode()
                    else:
                        print("Sending 404")
                        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                
        conn.sendall(response)    
        conn.close()

if __name__ == "__main__":
    main()
