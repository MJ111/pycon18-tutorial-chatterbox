import asyncio
import datetime
import uuid

from sanic import Sanic
import json

from websockets import ConnectionClosed

app = Sanic()

UUID_NAMESPACE = uuid.uuid4()

connections = set()


@app.websocket('/feed')
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

        message_data = data['data']
        if 'schedule' in message_data:
            schedule_data = message_data['schedule']

            timedelta = {}
            if 'hours' in schedule_data:
                timedelta['hours'] = int(schedule_data['hours'])
            if 'minutes' in schedule_data:
                timedelta['minutes'] = int(schedule_data['minutes'])
            if 'seconds' in schedule_data:
                timedelta['seconds'] = int(schedule_data['seconds'])
            delay = int(datetime.timedelta(**timedelta).total_seconds())

            await asyncio.sleep(delay)
            data = {**data, "data": {"text": message_data["text"]}}
            await send(data, ws, schedule=True)
        else:
            await send(data, ws)


async def send(data, ws, schedule=False):
    data = json.dumps(data)
    print('Sending: ' + data)

    for connection in connections.copy():
        if connection != ws or schedule:
            try:
                await connection.send(data)
            except ConnectionClosed:
                if connection in connections:
                    connections.remove(connection)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
