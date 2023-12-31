import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import threading
import os

class ChatClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat Client")

        self.nickname = self.load_or_get_nickname()

        self.create_widgets()

        self.server_host = '127.0.0.1'
        self.server_port = 5555

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def create_widgets(self):
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=15)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.nickname_label = tk.Label(self.root, text=f"Your Name: {self.nickname}")
        self.nickname_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.message_label = tk.Label(self.root, text="Message:")
        self.message_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.change_name_button = tk.Button(self.root, text="Change Name", command=self.change_name)
        self.change_name_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)

    def load_or_get_nickname(self):
        filename = 'nickname.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return file.read().strip()
        else:
            return self.ask_nickname()

    def ask_nickname(self):
        nickname = tk.simpledialog.askstring("Name", "Enter your name:")
        if nickname:
            with open('nickname.txt', 'w') as file:
                file.write(nickname)
            return nickname
        else:
            self.root.destroy()
            raise SystemExit

    def connect_to_server(self):
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            tk.messagebox.showerror("Connection Error", f"Failed to connect to the server.\nError: {e}")
            self.root.destroy()

    def send_message(self):
        message = self.message_entry.get().strip()

        if message == '':
            tk.messagebox.showwarning("Warning", "Enter a message.")
            return

        chat_message = f'{self.nickname}: {message}'
        self.append_message(chat_message)

        try:
            self.client_socket.send(chat_message.encode('utf-8'))
        except Exception as e:
            tk.messagebox.showerror("Connection Error", f"Error sending message to the server.\nError: {e}")

        self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.append_message(message)
            except Exception as e:
                print(f"Error: {e}")
                break

    def append_message(self, message):
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.see(tk.END)

    def change_name(self):
        new_nickname = tk.simpledialog.askstring("Change Name", "Enter your new name:")
        if new_nickname:
            self.nickname = new_nickname
            self.nickname_label.config(text=f"Your Name: {self.nickname}")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.run()
