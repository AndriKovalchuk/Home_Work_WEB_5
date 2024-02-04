from aiofile import async_open
import asyncio
from datetime import datetime
from main import get_exchange_info
import socket


async def logging_to_file(command):
    async with async_open("log.txt", "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await file.write(f'{timestamp}: Received "{command}" command\n')


async def main():
    host = socket.gethostname()
    port = 5000

    commands = [
        "exchange 1",
        "exchange 2",
        "exchange 3",
        "exchange 4",
        "exchange 5",
        "exchange 6",
        "exchange 7",
        "exchange 8",
        "exchange 9",
        "exchange 10",
    ]

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Socket server is listening on {host}:{port}")

    socket_client, address = server_socket.accept()
    print(f"Accepted socket_client from {address}")

    while True:
        message = socket_client.recv(4096).decode()
        if not message:
            break

        if message.lower().strip() == "exchange":
            exchange_info = get_exchange_info()
            exchange_info_str = str(exchange_info).encode()
            socket_client.send(exchange_info_str)
            print(f"Received command: {message}")
            await logging_to_file(message)
        elif message.lower().strip() in commands:
            days = int(message.split()[-1])
            exchange_info = get_exchange_info(days)
            exchange_info_str = str(exchange_info).encode()
            socket_client.send(exchange_info_str)
            print(f"Received command: {message}")
            await logging_to_file(message)
        else:
            print(f"Received message: {message}")
            msg = input(">>> ")
            socket_client.send(msg.encode())

    socket_client.close()
    server_socket.close()


if __name__ == "__main__":
    asyncio.run(main())
