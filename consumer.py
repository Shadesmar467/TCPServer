import socket, sys, time

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc:
        sc.connect((host, port))
        #getting the consumer connection to display on server
        consumer_id = str(sc.getsockname())
        sc.sendall(consumer_id.encode()) #sending consumer connection information
        print(f"Consumer# connected to server at {host}:{port}")
        print("Consumer# started")
        #need to implement multiple consumers at a time
        time.sleep(3)#temporary solution

        while True:
            sc.sendall(b'[REQUEST]\n') #consumer sends ID to the server to let it know what it is
            print("[REQUEST]") # from the server for a task

            response = sc.recv(1024).decode().strip()
            print(response)
            time.sleep(1)

if __name__ == "__main__":
    main()
