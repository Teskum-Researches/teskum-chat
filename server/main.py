import asyncio
import websockets
import json
from config import port, is_local, host, is_secure

messages = [{"user": "System", "content": "Teskum chat 1.0"}]

async def echo(websocket):
    async for raw_message in websocket:
        try:
            # Ожидаем JSON
            data = json.loads(raw_message)

            if data.get("cmd") == "list":
                await websocket.send(json.dumps({"messages": messages}))
            elif data.get("cmd") == "send":
                user = data.get("user")
                content = data.get("content")
                if user and content:
                    messages.append({"user": user, "content": content})
                await websocket.send(json.dumps({"messages": messages}))
            else:
                await websocket.send(json.dumps({"error": "Unknown command"}))
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"error": "Invalid JSON"}))

async def main():
    print(" " + "=" * 16)
    print(" Teskum chat server starting...")
    if is_local:
        print("!Server running local")
        host_to_use = "localhost"
    else:
        host_to_use = host
    if not is_secure:
        print("!Server running unsecure")
    print(" port:", port)
    print(" " + "=" * 16)
    print(" Server started!")
    
    async with websockets.serve(
        echo,
        host_to_use,
        port,
        ping_interval=20,   # отправлять ping каждые 20 сек
        ping_timeout=10     # ждать pong 10 сек
    ) as server:
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())