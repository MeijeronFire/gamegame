import asyncio
import websockets
import time
import json

uuid = ""

def registerJson() -> str:
	return json.dumps({
		"type": "register",
		"name": "Evgeny",
		"timestamp": time.time()
	})

async def async_input(prompt: str = "") -> str:
	return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

async def client():
	global uuid
	uri = "ws://127.0.0.1:8000/ws"
	async with websockets.connect(uri, ping_interval=5, ping_timeout=10) as websocket:
		print("Connected to server")

		# register with server
		await websocket.send(registerJson())
		try:
			response = json.loads(await websocket.recv())
		except json.JSONDecodeError:
			await websocket.send(json.dumps({"error": "malformed json"}))
		print(f"Registered. UUID = {response["uuid"]}")


		while True:
			msg = await async_input("Enter message, q to quit: ")
			if msg.lower() == "q":
				print("Closing connection")
				break
			
			json_obj = {
				"type": msg,
				"name": "John",
				"timestamp": time.time()
			}
			await websocket.send(json.dumps(json_obj))
			
			try:
				response = json.loads(await websocket.recv())
			except json.JSONDecodeError:
				await websocket.send(json.dumps({"error": "malformed json"}))
				continue
			
			print(f"Received from server: {response}")

if __name__ == "__main__":
	asyncio.run(client())