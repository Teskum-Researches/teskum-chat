import asyncio
import websockets
import json
from config import ip, port, is_secure

async def hello():
    uri = f"{'wss' if is_secure else 'ws'}://{ip}:{port}/ws"
    async with websockets.connect(uri) as websocket:
        print("Username")
        user = input("> ").strip()
        while True:
            command = input("command> ").strip()
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
                content = input("  Content?> ").strip()
                await websocket.send(json.dumps({"cmd": "send", "user": user, "content": content}))
                response = await websocket.recv()
                data = json.loads(response)
                for msg in data.get("messages", []):
                    print(f"{msg['user']}: {msg['content']}")
            else:
                print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    asyncio.run(hello())