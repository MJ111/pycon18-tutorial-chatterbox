from sanic import Sanic
from chatterbox import chatterbox

app = Sanic()


@app.websocket('/')
async def chat(request, ws):
    await chatterbox.connect(request, ws)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, access_log=True)
