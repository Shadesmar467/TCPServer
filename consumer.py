import socket, sys, time

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    #:worker_name = sys.argv[3]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        sc.connect((host, port))
        #consumer_id = sc.recv(1024).decode().strip()

        #need to implement multiple consumers at a time

        while True:
            sc.sendall(b'[REQUEST]\n') #consumer sends ID to the server to let it know what it is
            print("[REQUEST]") # from the server for a task

            response = sc.recv(1024).decode().strip()
            print(response)
            time.sleep(1)

if __name__ == "__main__":
    main()
