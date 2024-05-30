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
            print(data)
            if not data: break
            conn.send(data)
    


if __name__ == "__main__":
    main()
