# client.py
import socket
import threading
import time

class Peer:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.messages = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 0))
        self.server_address = ("127.0.0.1", 5051)  # Change this to the server's IP address

    def send_message(self, msg):
        self.sock.sendto(f"{self.first_name} {self.last_name} {msg}".encode(), self.server_address)

    def receive_message(self):
        while True:
            data, _ = self.sock.recvfrom(1024)
            msg = data.decode().split(' ', 2)
            if len(msg) != 3:
                print("Invalid message format")
                continue
            first_name, last_name, message = msg
            timestamp = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
            self.messages[(first_name, last_name)] = {"message": message, "timestamp": timestamp}
            print(f"Received message from {first_name} {last_name} at {timestamp}")

    def display_messages(self):
        if not self.messages:
            print("No messages to display.")
            return
        print("Messages:")
        for i, ((first_name, last_name), msg) in enumerate(self.messages.items()):
            print(f"{i + 1}- From {first_name} {last_name} at {msg['timestamp']}: {msg['message']}")

def main():
    first_name = input("Enter your first name: ").capitalize()
    last_name = input("Enter your last name: ").capitalize()
    peer = Peer(first_name, last_name)

    receive_thread = threading.Thread(target=peer.receive_message)
    receive_thread.start()

    while True:
        message = input("Enter a message (or enter 'list' to display messages): ").strip()

        if message.lower() == "list":
            peer.display_messages()
        else:
            peer.send_message(message)


if __name__ == "__main__":
    main()
