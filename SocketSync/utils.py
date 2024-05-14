from flask import Flask


app = Flask()


@app.route("/")
def addew():
    return "hello world"

def data_formatter(response):
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


def get_args(data):
    _data = {}
    if len(data) <= 1:
        print('No argument supplied')
        return
    for args in data:
        if '=' in args:
            k, v = args.split('=')
            _data[k.strip()] = v.strip()
    return _data


def create_response(status_code, content_type, content):
    response = f'HTTP/1.1 {status_code}\r\n'
    response += f"Content-Type: {content_type}\r\n"
    response += f"\r\n"
    response += content
    return response
