#! /usr/bin/env python3
import asyncio
import websockets
import ssl
import json
from config import port, is_local, host, is_secure, cert_file, cert_key
from db import ChatDB

db = ChatDB()

messages = db.get_messages()

async def echo(websocket):
    async for raw_message in websocket:
        try:
            data = json.loads(raw_message)
            cmd = data.get("cmd")

            if cmd == "list":
                with ChatDB() as db:
                    messages = db.get_messages()
                await websocket.send(json.dumps({"messages": messages}))

            elif cmd == "send":
                user = data.get("user")
                content = data.get("content")
                if user and content:
                    with ChatDB() as db:
                        db.add_message(user=user, text=content)
                        messages = db.get_messages()
                    await websocket.send(json.dumps({"messages": messages}))
                else:
                    await websocket.send(json.dumps({"error": "Missing user or content"}))

            else:
                await websocket.send(json.dumps({"error": "Unknown command"}))

        except json.JSONDecodeError:
            await websocket.send(json.dumps({"error": "Invalid JSON"}))

async def main():
    #print(" " + "=" * 16)
    print("Teskum chat: server version 1.0 is starting...")
    if is_local:
        print("Server is running local")
        host_to_use = "localhost"
    else:
        host_to_use = host
    if not is_secure:
        print("Server is running unsecure")
    print("port:", port)
    #print(" " + "=" * 16)
    print("Server started!")
    
    if not is_secure:
        ssl_context = None
    else:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(cert_file, cert_key)
    async with websockets.serve(
        echo,
        host_to_use,
        port,
        ping_interval=20,   # отправлять ping каждые 20 сек
        ping_timeout=10,# ждать pong 10 сек
        ssl=ssl_context
    ) as server:
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
