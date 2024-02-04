from datetime import datetime
import socket


def main():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))
    message = input(">>> ")

    while message.lower().strip() != "exit":
        client_socket.send(message.encode())
        msg = client_socket.recv(4096).decode()

        if "exchange" == message.lower():
            print(
                f'The conversion rate for the Ukrainian Hryvnia (UAH) to various currencies on {datetime.now().date().strftime("%d.%m.%Y")}:\n{msg}'
            )
        else:
            print(f"Received message: \n{msg}")

        message = input(">>> ")


if __name__ == "__main__":
    main()
