import asyncio
import websockets #type: ignore
from config import ip, port, is_secure

async def hello():
    if is_secure:
        uri = f"wss://{ip}:{port}/ws"
    else:
        uri = f"ws://{ip}:{port}/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        response = await websocket.recv()
        print(f"Response from server: {response}")

if __name__ == "__main__":
    asyncio.run(hello())
