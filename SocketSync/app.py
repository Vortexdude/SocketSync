import socket

SOCKET_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM


class App:
    BUFFER_SIZE = 1024

    def __init__(self, address: str = '127.0.0.1', port: int = 5000):
        self.address = address
        self.port = port
        self.endpoints = []
        self.server = socket.socket(SOCKET_FAMILY, SOCKET_TYPE)
        self.server.bind((self.address, self.port))
        self.server.listen(0)
        print(f"Listening on {self.address}:{self.port}")

    def route(self, endpoint):
        def decorator(function):
            def wrapper(*args, **kwargs):
                print(f'{self.endpoints=}')
                self.endpoints.append(endpoint)
                print(f'{self.endpoints=}')
                return function(*args, **kwargs)

            return wrapper

        return decorator

    def run_server(self):
        while True:
            client_socket, client_addr = self.server.accept()
            print("Connection from:", client_addr)
            try:
                request_data = client_socket.recv(self.BUFFER_SIZE).decode()
                formatted_data: dict = self.data_formatter(request_data)
                endpoint = formatted_data['request'][1]
                if endpoint not in self.endpoints:
                    response_content = f"<h1>You are Not allow to view the page {endpoint}</h1>"
                    status_code = '404 Not Found'
                else:
                    response_content = f"Welcome to our first website"
                    status_code = '200 OK'

                http_request = self.create_response(status_code, "text/html", response_content)
                client_socket.sendall(http_request.encode())

            except OSError as e:
                raise Exception(e)

            client_socket.close()

    @staticmethod
    def data_formatter(response) -> dict:
        data_dict = {}
        for line in response.split('\n'):
            if not line.strip():
                continue
            if len(line.split(":", 1)) <= 1:
                data_dict['request'] = line.split()
                continue
            key, value = line.split(':', 1)
            data_dict[key.strip()] = value.strip()
        return data_dict

    @staticmethod
    def create_response(status_code, content_type, content):
        response = f'HTTP/1.1 {status_code}\r\n'
        response += f"Content-Type: {content_type}\r\n"
        response += f"\r\n"
        response += content
        return response
