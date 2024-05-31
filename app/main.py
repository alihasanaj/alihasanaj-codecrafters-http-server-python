# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    (conn, address) = server_socket.accept() # wait for client
    
    with conn:
        val = conn.recv(1024)
        pars = val.decode()
        args = pars.split("\r\n")
        print(args)
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        if len(args) > 1:
            path = args[0].split(" ")
            if path[1] == "/":
                response = b"HTTP/1.1 200 OK\r\n\r\n"
            if "echo" in path[1]:
                string = path[1].strip("/echo/")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
            if "user" in path[1]:
                path = args[2]
                print(path)
                string = path.strip("User-Agent")
                response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(string)}\r\n\r\n{string}".encode()
                
        print(f"Recived: {val}")
        conn.sendall(response)    
        
    
    server_socket.close()

if __name__ == "__main__":
    main()
