# Uncomment this to pass the first stage
import socket
import threading
import os
import sys
import gzip

# Global 
# Default responses
response_200 = f"HTTP/1.1 200 OK\r\n\r\n"
response_404 = f"HTTP/1.1 404 Not Found\r\n\r\n"

# Custom responses
response_201 = f"HTTP/1.1 201 Created\r\n\r\n".encode()

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
        

def echo_request(request, encoding_check):
    if request == "/":
        return response_200
    else:
        string = request.replace("/echo/", "")
        if "Encoding" in encoding_check:
            string = gzip.compress(string.encode("utf-8"))
            encoding_type = encoding_check.replace("Accept-Encoding: ", "")
            if "," in encoding_type:
                encoding_type = encoding_check.replace(" ", "")
                encoding_type = encoding_type.split(",")
            
            
            print(encoding_type)
            if "gzip" == encoding_type:
                return  f"HTTP/1.1 200 OK\r\nContent-Encoding: {encoding_type}\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n".encode() + string
            elif "gzip" in encoding_type:
                index = encoding_type.index("gzip")
                return f"HTTP/1.1 200 OK\r\nContent-Encoding: {encoding_type[index]}\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            else:
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
        else:
            return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
        


def post_request():
    pass    
    
def request_handler(conn: socket.socket):
        client_data = conn.recv(1024)
        decoded_data = client_data.decode()
        arguments = decoded_data.split("\r\n")
        print(f"arguments: {arguments}")
        # Split the request line and extract http info
        request_line = arguments[0].split(" ")
        http_method = request_line[0]
        request_target = request_line[1]
        http_version = request_line[2]
        
        # Split the headers line
        header_host = arguments[1]
        user_agent = arguments[2]
        media_type = arguments[-2]
        req_body = arguments[-1]
        
        print(f"http method: {http_method}")
        print(f"request target: {request_target}")
        print(f"http version: {http_version}")
        
        print(f"{header_host}")
        print(f"Agent: {user_agent}")
        print(f"Type: {media_type}")
        print(f"Body: {req_body}")
            
            
        
        
        
        # supported encoding
        supported_encodes = ["gzip"]
        
        response = response_404
        if "echo" in request_target:
            response = echo_request(request=request_target, encoding_check=user_agent) 
        elif "files" in request_target:
                if "POST" in http_method:
                    directory = sys.argv[2]
                    try:
                        os.mkdir(directory)
                    except FileExistsError as e:
                        print(f"Directory {directory} already exist")
                    file = request_target.replace("/files/", "")
                    body = req_body
                    with open(os.path.join(directory, file), "w") as f:
                        f.write(body)
                    response = response_201
                else:
                    directory = sys.argv[2]
                    file = request_target.replace("/files/", "")
                    if os.path.isfile(f"/{directory}/{file}"):
                        with open(f"/{directory}/{file}", "r") as f:
                            lines = ""
                            for word in f:
                                lines += word
                            lines_len = len(lines)
                        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {lines_len}\r\n\r\n{lines}".encode()
                    else:
                        response = response_404
        print(f"Response Sent: {response}")   
        conn.sendall(response)
        conn.close()

if __name__ == "__main__":
    main()
