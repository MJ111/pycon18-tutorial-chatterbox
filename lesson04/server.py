import uuid

from sanic import Sanic
import json

from websockets import ConnectionClosed

app = Sanic()

UUID_NAMESPACE = uuid.uuid4()

connections = set()


@app.websocket('/')
async def feed(request, ws):
    connections.add(ws)
    unique_id = uuid.uuid3(UUID_NAMESPACE, request.ip).hex
    await ws.send(json.dumps({"id": unique_id}))  # send unique id to client
    while True:
        try:
            data = await ws.recv()
        except ConnectionClosed:
            if ws in connections:
                connections.remove(ws)
            break

        print('Received: ' + data)
        data = json.loads(data)
        data['author'] = unique_id
        data = json.dumps(data)
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
