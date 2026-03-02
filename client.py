import asyncio
import websockets
import time
import json

async def client():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        # log status
        print("Connected to server")
        while True:
            msg = input("Enter message to send, q to quit: ")
            if msg.lower() == "q":
                print("Closing connection")
                break
            
            json_obj = {
                "msg": msg,
                "timestamp": time.time()
            }
            await websocket.send(json.dumps(json_obj))
            response = json.loads(await websocket.recv())
            print(f"Received from server: {response}")

if __name__ == "__main__":
    asyncio.run(client())