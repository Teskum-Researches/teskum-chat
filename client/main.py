import asyncio
import websockets
import json
from config import ip, port, is_secure

async def ainput(prompt: str = "") -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)

async def hello():
    uri = f"{'wss' if is_secure else 'ws'}://{ip}:{port}/ws"
    async with websockets.connect(uri, ping_interval=20, ping_timeout=10) as websocket:
        print("Username")
        user = (await ainput("> ")).strip()
        while True:
            command = (await ainput("command> ")).strip()
            if command == "help":
                print("Teskum chat 1.0")
                print("help = command list")
                print("list = list messages")
                print("send = sends a message")
            elif command == "list":
                await websocket.send(json.dumps({"cmd": "list"}))
                response = await websocket.recv()
                data = json.loads(response)
                for msg in data.get("messages", []):
                    print(f"{msg['user']}: {msg['content']}")
            elif command == "send":
                content = (await ainput("  Content?> ")).strip()
                await websocket.send(json.dumps({"cmd": "send", "user": user, "content": content}))
                response = await websocket.recv()
                data = json.loads(response)
                for msg in data.get("messages", []):
                    print(f"{msg['user']}: {msg['content']}")
            else:
                print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    asyncio.run(hello())