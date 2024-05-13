from webcrawler import Webcrawler

from asyncio import Future
from websockets.server import serve

RETRY_COUNT = 3
BACKOFF_TIME = 1

PORT = 8000
HOST_IP = "0.0.0.0"

async def websocket_server(websocket):
    async for message in websocket:
        print("Connection Received")

        temp = Webcrawler(RETRY_COUNT, BACKOFF_TIME, message, websocket)
        await temp.get_all_links_from_url()


async def init_server():
    print("Starting websocket...")
    async with serve(websocket_server, HOST_IP, PORT):
        await Future()
