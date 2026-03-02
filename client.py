import asyncio
import websockets

async def client():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")
        while True:
            msg = input("Enter message to send: ")
            if msg.lower() == "quit":
                print("Closing connection")
                break
            await websocket.send(msg)
            response = await websocket.recv()
            print(f"Received from server: {response}")

if __name__ == "__main__":
    asyncio.run(client())