import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))

    print("Connected to server.")

    choice = input("Choose 'signup' or 'login': ").lower()
    while choice not in ['signup', 'login']:
        print("Invalid choice. Please choose 'signup' or 'login'.")
        choice = input("Choose 'signup' or 'login': ").lower()

    client_socket.send(choice.encode())

    if choice == 'signup':
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Are you an owner or a customer? Enter 'owner' or 'customer': ")
        signup_data = f"{username}:{password}:{role}"
        client_socket.send(signup_data.encode())
    elif choice == 'login':
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_data = f"{username}:{password}"
        client_socket.send(login_data.encode())
        login_response = client_socket.recv(1024).decode()
        login_parts = login_response.split("|")
        if len(login_parts) == 2 and login_parts[0] == 'Login successful':
            role_flag = login_parts[1]
            print(f"Logged in as {role_flag}")
            if role_flag == 'owner':
                action = input("Choose 'add_menu_item' or 'modify_menu_item': ").lower()
                while action not in ['add_menu_item', 'modify_menu_item']:
                    print("Invalid choice. Please choose 'add_menu_item' or 'modify_menu_item'.")
                    action = input("Choose 'add_menu_item' or 'modify_menu_item': ").lower()
                client_socket.send(action.encode())
                if action == 'add_menu_item' or action == 'modify_menu_item':
                    item_name = input("Enter the item name: ")
                    item_price = input("Enter the item price: ")
                    item_data = f"{item_name}:{item_price}"
                    client_socket.send(item_data.encode())
                    menu_update_response = client_socket.recv(1024).decode()
                    print(menu_update_response)
        else:
            print(login_response)

    response = client_socket.recv(1024).decode()
    print(response)

    client_socket.close()

if __name__ == "__main__":
    main()
