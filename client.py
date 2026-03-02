import asyncio
import websockets
import time
import json


class Client:
	def __init__(self):
		self.connection = None
		self.uuid = None
		self.url = None # "ws://127.0.0.1:8000/ws"
		self.name = "Evgeny"
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.loop)

	async def _connect(self):
		self.connection = await websockets.connect(self.url, ping_interval=20, ping_timeout=10)

	def connect(self):
		self.loop.run_until_complete(self._connect())
		print("connected to server!")

	async def _send(self, payload: dict):
		await self.connection.send(json.dumps(payload))
	
	async def _send_receive(self, payload: dict) -> dict:
		await self.connection.send(json.dumps(payload))
		while 1:
			msg = await self.connection.recv()
			data = json.loads(msg)
			if data["type"] == "regResp":
				return data
	
	def register(self, name: str):
		payload = {
			"type": "register",
			"name": name,
			"timestamp": time.time()
		}
		self.uuid = self.loop.run_until_complete(
			self._send_receive(payload)
		)["uuid"]
		print(self.uuid)

	async def _async_input(prompt: str = "") -> str:
		return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

	async def _listen(self, callback):
		async for message in self.connection:
			try:
				response = json.loads(message)
			except json.JSONDecodeError:
				self._send({"type": "error", "error": "malformed json"})
			callback(message)
	
	def on_message(self, callback: callable):
		asyncio.ensure_future(self._listen(callback))

if __name__ == "__main__":
	client = Client()
	client.url = "ws://127.0.0.1:8000/ws"
	client.connect()
	client.register("Otto")