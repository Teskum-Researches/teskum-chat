import asyncio
import websockets # type: ignore
from config import port, is_local, host

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"Server received: {message}")

async def main():
    global host
    if is_local:
        host = "localhost"
    async with websockets.serve(echo, host, port):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
