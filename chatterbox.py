import asyncio
import datetime
import json
import threading
import uuid

from sanic import log
from websockets import ConnectionClosed

from room import Room

logger = log.logger


class ChatterBox:

    def __init__(self):
        self._connections = []
        self._rooms = []
        self._UUID_NAMESPACE = uuid.uuid4()
        self._lock = threading.Lock()

    async def _receive(self, ws):
        try:
            data = await ws.recv()
        except ConnectionClosed:
            if ws in self._connections:
                self._connections.remove(ws)
            raise

        logger.info('Received: ' + data)
        return data

    async def _broadcast(self, data, ws, schedule=False):
        data = json.dumps(data)
        logger.info('Sending: ' + data)

        idx = 0
        while True:
            if idx == len(self._connections):
                break

            connection = self._connections[idx]

            if connection != ws or schedule:
                try:
                    await connection.send(data)
                except ConnectionClosed:
                    if connection in self._connections:
                        self._connections.remove(connection)

            idx += 1

    async def connect(self, request, ws):
        self._connections.append(ws)

        unique_id = uuid.uuid3(self._UUID_NAMESPACE, request.ip).hex
        await ws.send(json.dumps({"id": unique_id}))  # send unique id to client

        await self._feed(ws, unique_id)

    async def _feed(self, ws, unique_id):
        while True:
            try:
                data = await self._receive(ws)
            except ConnectionClosed:
                return

            data = json.loads(data)
            if 'channel' in data:
                break

            data = self._prepare(data, unique_id)

            schedule_data = self._get_schedule_data(data)
            if schedule_data:
                delay, data = schedule_data
                await asyncio.sleep(delay)
                await self._broadcast(data, ws, schedule=True)
            else:
                await self._broadcast(data, ws)

        if data['channel'] == 'random':
            await self._random(ws, unique_id)

    async def _join_room(self, ws):
        while not self._lock.acquire(blocking=False):
            await asyncio.sleep(1)
        joined_room: Room = None

        idx = 0
        while True:
            if idx == len(self._rooms):
                break

            room = self._rooms[idx]

            if len(room) < 2:  # for 1:1 room
                room.join(ws)
                joined_room = room
                break

            idx += 1

        if joined_room is None:
            room = Room()
            self._rooms.append(room)

            room.join(ws)
            joined_room = room
        self._lock.release()

        return joined_room

    async def _random(self, ws, unique_id):
        self._connections.remove(ws)
        joined_room = await self._join_room(ws)

        while True:
            try:
                data = await self._receive(ws)
            except ConnectionClosed:
                return

            data = json.loads(data)
            if 'channel' in data:
                break

            data = self._prepare(data, unique_id)

            schedule_data = self._get_schedule_data(data)
            if schedule_data:
                delay, data = schedule_data
                await asyncio.sleep(delay)
                await joined_room.send_message(data, ws, schedule=True)
            else:
                await joined_room.send_message(data, ws)

        if data['channel'] == 'feed':
            await self._feed(ws, unique_id)

    @classmethod
    def _prepare(cls, data, unique_id):
        data['author'] = unique_id
        return data

    @classmethod
    def _get_schedule_data(cls, data):
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

            data = {**data, "data": {"text": message_data["text"]}}

            return delay, data
        return


chatterbox = ChatterBox()
