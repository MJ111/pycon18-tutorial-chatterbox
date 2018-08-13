from sanic import Sanic
import json

app = Sanic()

@app.websocket('/chat')
async def feed(request, ws):
    while True:
        data = await ws.recv()
        print('Received: ' + data)
        data = json.loads(data)
        data['author'] = 'them'
        data = json.dumps(data)
        print('Sending: ' + data)
        await ws.send(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)