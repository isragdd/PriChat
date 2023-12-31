import socket
import threading

class ChatServer:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()

            print(f'Server listening on {self.host}:{self.port}')

            while True:
                client_socket, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()

        except Exception as e:
            print(f"Error: {e}")

    def handle_client(self, client_socket):
        nickname = client_socket.recv(1024).decode('utf-8')

        print(f'{nickname} connected from {client_socket.getpeername()}')

        message = f'{nickname} connected from {client_socket.getpeername()}.'
        self.broadcast(message, client_socket)

        self.clients.append((client_socket, nickname))

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break

                print(message)

                self.broadcast(message, client_socket)

            except Exception as e:
                print(f"Error: {e}")
                break

        print(f'{nickname} disconnected from {client_socket.getpeername()}')

        message = f'{nickname} disconnected.'
        self.broadcast(message, client_socket)

        self.clients.remove((client_socket, nickname))
        client_socket.close()

    def broadcast(self, message, sender_socket):
        for client_socket, _ in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start_server()
