from SocketSync.app import App

app = App()


@app.route('/')
def greetings():
    return {
        'message': "Nothing",
        'status_code': 200
    }


greetings()

app.run_server()
