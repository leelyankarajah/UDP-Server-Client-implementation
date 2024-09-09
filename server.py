# server.py
import socket
import threading
import time

class Display:
    def __init__(self, first_name, last_name, message, timestamp):
        self.first_name = first_name
        self.last_name = last_name
        self.message = message
        self.timestamp = timestamp

messages = {}
message_lock = threading.Lock()

def handle_client(sock, addr):
    while True:
        data, _ = sock.recvfrom(1024)
        message = data.decode().split(' ', 2)
        if len(message) != 3:
            print("Invalid message format")
            continue
        first_name, last_name, msg = message
        timestamp = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        with message_lock:
            messages[(first_name, last_name)] = Display(first_name, last_name, msg, timestamp)
            print(f"Received message from {first_name} {last_name} at {timestamp}")
            display_messages()

def display_messages():
    if not messages:
        print("No messages to display.")
        return
    print("Messages:")
    for i, (_, display) in enumerate(messages.items()):
        print(f"{i + 1}- From {display.first_name} {display.last_name} at {display.timestamp}: {display.message}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 5051))
    print("Server listening on port 5051")

    while True:
        data, addr = sock.recvfrom(1024)
        client_thread = threading.Thread(target=handle_client, args=(sock, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
