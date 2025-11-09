import socket, sys, time

from queue import PriorityQueue
from threading import Thread

def setup_sockets(ip, p, c):
    #initializing sockets and ports
    #producer
    p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p_socket.bind((ip, p))
    p_socket.listen(1)
    print("[SERVER] Producer listening on", p)

    #consumer
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.bind((ip, c))
    c_socket.listen(1)
    print("[SERVER] Consumer listening on", c)

    return p_socket, c_socket

def producer_worker(queue, sock):
    connSocket, addr = sock.accept()
    buffer = ""

    while True:
        data = connSocket.recv(1024).decode()
        if not data:
            break

        buffer += data

        # process all complete messages
        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)
            message = message.strip().split()
            #now message is an array of the 4 values on each line {timestamp, priority, task_id, duration}
            if message: # if a valid message exists:
                priority = message[1]
                task_ID = message[2]
                print(message)
                queue.put_nowait((priority, task_ID))

def consumer_worker(queue, sock):
    connSocket, addr = sock.accept()

    while True:
        #gets and removes tuple data from queue while full
        if ((connSocket.recv(2048)) and (not queue.empty())):
            taskData = queue.get()
            print(taskData)
            connSocket.sendall(b"[COMPLETE] " + taskData[1].encode() + b'\n')
        else:
            connSocket.sendall(b"NOTASK")

def shutdown(pSock, cSock):
    is_running = False
    print("\nexit")
    #close sockets, stop threads, save data
    pSock.close()
    cSock.close()

if __name__ == "__main__":

    q = PriorityQueue() 

    serverIP = sys.argv[1]
    prodPort = int(sys.argv[2])
    conPort = int(sys.argv[3])

    prodSock, conSock = setup_sockets(serverIP, prodPort, conPort)

    is_running = True;
    print("[SERVER] Server is running...")

    producer_thread = Thread(target=producer_worker, args=(q, prodSock), daemon=True)
    producer_thread.start()

    worker_thread = Thread(target=consumer_worker, args=(q, conSock), daemon=True)
    worker_thread.start()

    try:
        while is_running:
            #put polling and checking here
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(prodSock, conSock)

