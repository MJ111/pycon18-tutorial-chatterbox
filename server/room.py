import json

from websockets import ConnectionClosed


class Room:

    def __init__(self):
        self._connections = []

    def join(self, connection):
        self._connections.append(connection)

    def leave(self, connection):
        if connection in self._connections:
            self._connections.remove(connection)

    async def send_message(self, message, ws, schedule=False):
        message = json.dumps(message)

        idx = 0
        while True:
            if idx == len(self._connections):
                break

            connection = self._connections[idx]
            if connection != ws or schedule:
                try:
                    await connection.send(message)
                except ConnectionClosed:
                    self.leave(connection)

            idx += 1

    def __len__(self):
        return len(self._connections)
