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
        print("Connected by", address)
        while True:
            data = conn.recv(1024)
            if not data: break
            start = data.find(b'/echo/') + 6
            end = data.find(b"HTTP", start)
            result = data[start:end]
            print(result)
            
            if b"GET / HTTP" in data:
                conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
    
    server_socket.close()

if __name__ == "__main__":
    main()
