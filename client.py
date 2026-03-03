import asyncio
import websockets
import time
import json
from random import randint

class Client:
	def __init__(self):
		self.connection = None
		self.uuid = None
		self.url = None # "ws://127.0.0.1:8000/ws"
		self.name = "Evgeny"
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.loop)
		self._callbacks = []

	async def _async_input(self, prompt: str = "") -> str:
		return await asyncio.get_event_loop().run_in_executor(None, input, prompt)

	def async_input(self, prompt: str = "") -> str:
		return self.loop.run_until_complete(self._async_input(prompt))

	async def _connect(self):
		self.connection = await websockets.connect(self.url, ping_interval=20, ping_timeout=10)

	def connect(self):
		self.loop.run_until_complete(self._connect())
		print("connected to server!")

	async def _send(self, payload: dict):
		await self.connection.send(json.dumps(payload))
	
	def send(self, action: str, **data):
		payload = {
			"type" : action,
			"uuid" : self.uuid,
			"name" : self.name,
			"timestamp" : time.time(),
			**data
		}
		print(f"sending {payload}")
		return self.loop.run_until_complete(self._send(payload))

	async def _listen(self):
		"""
		Waits for all incoming messages and handles them
		"""
		async for message in self.connection:
			try:
				response = json.loads(message)
			except json.JSONDecodeError:
				await self._send({"type": "error", "error": "malformed json"})
				continue
			
			for callback in self._callbacks:
				callback(response)
	def listener(self, func: callable):
		"""
		Decorator. Used with:
			@Client.listener
			def something():
				...
		"""
		self._callbacks.append(func)
		return func

	async def _send_receive(self, payload: dict) -> dict:
		await self.connection.send(json.dumps(payload))
		while 1:
			msg = await self.connection.recv()
			data = json.loads(msg)
			if data["type"] == "regResp":
				return data
	
	def register(self):
		payload = {
			"type": "register",
			"name": self.name,
			"timestamp": time.time()
		}
		self.uuid = self.loop.run_until_complete(
			self._send_receive(payload)
		)["uuid"]
		print(self.uuid)
	
	def on_message(self, func: callable):
		self._handler = func
		return func

	def run(self):
		async def main():
			self.connect()
			self.register()
			self._listener_task = asyncio.create_task(self._listen())
			await self._listener_task
		self.loop.run_until_complete(main())

client = Client()

@client.listener
def customListener(msg):
	print(f"anker anker {msg}")

client.url = "ws://127.0.0.1:8000/ws"
client.name = str(randint(0, 10000))
client.run()
while 1:
	val = client.async_input()
	client.send(
		action = "getState",
		some = val
	)