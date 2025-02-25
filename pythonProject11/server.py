import socket
import json
import os.path

MENU_FILE = "menu.json"
USERS_FILE = "users.json"  # File to store user credentials

def load_menu():
    if os.path.isfile(MENU_FILE):
        with open(MENU_FILE, "r") as file:
            return json.load(file)
    else:
        return []

def save_menu(menu):
    with open(MENU_FILE, "w") as file:
        json.dump(menu, file)

def load_users():
    if os.path.isfile(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)

def handle_client(client_socket, menu, users):
    # Receive choice between signup and login
    choice = client_socket.recv(1024).decode()

    if choice == 'signup':
        # Receive signup details (username, password, role)
        username, password, role = client_socket.recv(1024).decode().split(":")
        # Check if the username already exists
        if username in users:
            client_socket.send("Username already exists".encode())
            return
        # Save the user details to the users file
        users[username] = {"password": password, "role": role}
        save_users(users)
        client_socket.send("Signup successful".encode())
    elif choice == 'login':
        # Receive login details (username, password)
        username, password = client_socket.recv(1024).decode().split(":")
        # Check if the username exists and the password matches
        if username in users and users[username]["password"] == password:
            client_socket.send("Login successful".encode())
        else:
            client_socket.send("Invalid credentials".encode())

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)

    print("Server started. Listening for connections...")

    menu = load_menu()
    users = load_users()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established.")

        handle_client(client_socket, menu, users)

        client_socket.close()

if __name__ == "__main__":
    main()
