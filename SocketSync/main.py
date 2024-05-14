import socket
from utils import data_formatter, get_args, create_response
import sys
import os

SOCKET_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM
LISTEN_PORT = 8080
SERVER_IP = '127.0.0.1'
BUFFER_SIZE = 1024

mapped_endpoint = [
    '/favicon.ico'
    '/',
    '/hello',
    '/index.html'
]


def run_server():
    global LISTEN_PORT
    conf = get_args(sys.argv)
    if conf['port']:
        LISTEN_PORT = int(conf['port'])
    server = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
    server.bind((SERVER_IP, LISTEN_PORT))

    # https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.listen(0)
    print(f"Listening on {SERVER_IP}:{LISTEN_PORT}")

    while True:
        client_socket, client_address = server.accept()
        print("Connection from:", client_address)

        try:
            request_data = client_socket.recv(BUFFER_SIZE).decode()
            formatted_data = data_formatter(request_data)
            endpoint = formatted_data['request'][1]
            if endpoint not in mapped_endpoint:
                response_content = f"<h1>You are Not allow to view the page {endpoint}</h1>"
                status_code = '404 Not Found'
            else:

                if '.html' in endpoint:
                    file = endpoint.split('/')[1]
                    current_working_dir = os.getcwd()
                    static_file = os.path.join(current_working_dir, 'SocketSync', 'static', file)
                    with open(static_file) as f:
                        response_content = f.read()
                    status_code = "200 OK"
                else:
                    response_content = f"You are visiting {formatted_data['request'][1]}"
                    status_code = "200 OK"

            http_response = create_response(status_code, "text/html", response_content)

            client_socket.sendall(http_response.encode())
        except OSError as e:
            print("Error:", e)

        client_socket.close()


run_server()
