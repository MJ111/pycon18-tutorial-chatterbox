from sanic import Sanic
import json

app = Sanic()

@app.websocket('/chat')
async def feed(request, ws):
    while True:
        data = await ws.recv()
        print('Received: ' + data)
        data = json.dumps({"type": "text", "author": "random", "data": 'hello!'})
        print('Sending: ' + data)
        await ws.send(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)