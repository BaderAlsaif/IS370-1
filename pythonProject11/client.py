import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))

    # Choose between signup and login
    choice = input("Choose 'signup' or 'login': ")
    while choice not in ['signup', 'login']:
        print("Invalid choice. Please choose 'signup' or 'login'.")
        choice = input("Choose 'signup' or 'login': ")

    # Send choice to the server
    client_socket.send(choice.encode())

    # Handle signup or login based on the choice
    if choice == 'signup':
        # Ask for signup details
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Are you an owner or a customer? Enter 'owner' or 'customer': ")
        # Send signup details to the server
        signup_data = f"{username}:{password}:{role}"
        client_socket.send(signup_data.encode())
    elif choice == 'login':
        # Ask for login details
        username = input("Enter username: ")
        password = input("Enter password: ")
        # Send login details to the server
        login_data = f"{username}:{password}"
        client_socket.send(login_data.encode())

    response = client_socket.recv(1024).decode()
    print(response)

    client_socket.close()

if __name__ == "__main__":
    main()
