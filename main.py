from datetime import datetime, timedelta
import logging
from pathlib import Path
import socket
from threading import Thread

import httpx

BASE_DIR = Path()
BUFFER_SIZE = 4096
HTTP_PORT = 3000
HTTP_HOST = '0.0.0.0'
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 5000


def request(url: str):
    with httpx.Client(timeout=60) as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


def get_exchange_info(days: int = None):
    if not days:
        current_date = datetime.now().date()
        result = ""

        try:
            response = request(
                "https://api.privatbank.ua/p24api/exchange_rates?date=" + current_date.strftime("%d.%m.%Y")
            )

            exchange_rate_values = [v for v in response.get("exchangeRate")]

            for val_dict in exchange_rate_values:
                currency = val_dict.get("currency")
                if val_dict.get("saleRate") is not None:
                    exchange_dict = {
                        "sale": val_dict.get("saleRate"),
                        "purchase": val_dict.get("purchaseRate"),
                    }

                    format_ = (f"{currency}:  "
                               f"sale: {exchange_dict.get('sale')}, "
                               f"purchase: {exchange_dict.get('purchase')}\n")
                    result += format_

            return result

        except Exception as err:
            print(f"Error fetching exchange information: {err}")
            return
    else:
        current_date = datetime.now().date()
        delta = timedelta(days=days)
        delta_1 = timedelta(days=1)
        check_date = current_date - delta

        try:

            new_list = []
            while check_date <= (current_date - delta_1):
                result = f'{check_date.strftime('%d.%m.%Y')}: '
                response = request(
                    "https://api.privatbank.ua/p24api/exchange_rates?date=" + check_date.strftime("%d.%m.%Y")
                )

                exchange_rate_values = [v for v in response.get("exchangeRate")]

                for val_dict in exchange_rate_values:

                    currency = val_dict.get("currency")
                    if val_dict.get("saleRate") is not None:
                        exchange_dict = {
                            "sale": val_dict.get("saleRate"),
                            "purchase": val_dict.get("purchaseRate"),
                        }

                        format_ = (f"{currency}: "
                                   f"sale: {exchange_dict.get('sale')}, "
                                   f"purchase: {exchange_dict.get('purchase')}; ")
                        result += format_

                new_list.append(result)
                check_date += delta_1
            result = "\n".join(new_list)
            return result

        except Exception as err:
            print(f"Error fetching exchange information: {err}")
            return


def run_socket_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    logging.info('Starting Socket-server...')
    try:
        while True:
            message, address = server_socket.recvfrom(BUFFER_SIZE)
            logging.info(f'Socket received: {address}: {message}')
            # save_data_from_form(message)
    except KeyboardInterrupt:
        pass
    finally:
        server_socket.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

    server_socket = Thread(target=run_socket_server, args=(SOCKET_HOST, SOCKET_PORT))
    server_socket.start()
