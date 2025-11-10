import socket, time, sys

def sendTasks(socket, tasks, start):
#sending tasks according to the timestamp provided
    #calculating correct time
    for timestamp, priority, task_id, duration in tasks:
        now = time.time()
        wait_time = timestamp - (now - start)
        if (wait_time > 0):
            time.sleep(wait_time)
        socket.sendall(f'[CREATE] {priority} {task_id} {duration}\n'.encode()) #server will receive and know to create a task and add it to queue



def main():
    start_time = time.time()
    host = sys.argv[1]
    port = int(sys.argv[2])
    task_file = sys.argv[3]

    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    tasks = []

    with open(task_file, "r") as f:
        for line in f:
            parts = line.split() #array of each word separated by " " e.g. ["0.0", "3", "task2", "2.0"]
            #breaking part apart and assigning timestamp, priority, task_id, duration
            timestamp = float(parts[0])
            priority = int(parts[1])
            task_id = parts[2]
            duration = float(parts[3])
            tasks.append((timestamp, priority, task_id, duration))
    
    sendTasks(sc, tasks, start_time)
  
if __name__ == "__main__":
    main()
