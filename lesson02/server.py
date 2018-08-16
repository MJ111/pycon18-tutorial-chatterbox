from sanic import Sanic

app = Sanic()

connections = set()


@app.websocket('/')
async def feed(request, ws):
    connections.add(ws)
    while True:
        data = await ws.recv()
        print('Received: ' + data)
        print('Sending: ' + data)
        await ws.send(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
