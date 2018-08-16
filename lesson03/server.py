from sanic import Sanic

from websockets import ConnectionClosed

app = Sanic()

connections = set()


@app.websocket('/')
async def feed(request, ws):
    connections.add(ws)
    while True:
        try:
            data = await ws.recv()
        except ConnectionClosed:
            if ws in connections:
                connections.remove(ws)
            break

        print('Received: ' + data)
        print('Sending: ' + data)

        for connection in connections.copy():
            if connection != ws:
                try:
                    await connection.send(data)
                except ConnectionClosed:
                    if connection in connections:
                        connections.remove(connection)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
