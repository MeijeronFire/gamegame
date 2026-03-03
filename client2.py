#!/usr/bin/env python3

import asyncio
import websockets
import time
import json
import inspect
from random import randint

class Client:
	def __init__(self):
		self.connection = None
		self.uuid = None
		self.url = None # "ws://127.0.0.1:8000/ws"
		self.name = "Evgeny"
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.loop)
		self._listeners = {}
		self.latest = None
	
	def on(self, action: str):
		def decorator(func):
			# if self._listeners["action"] is empty, initialize it
			self._listeners.setdefault(action, []).append(func)
			return func
		return decorator
	
	async def _connect(self):
		self.connection = await websockets.connect(self.url, ping_interval=20, ping_timeout=10)
		print("connected to server!")

	async def _send(self, action: str, **payload):
		packet = {
			"type" : action,
			"uuid" : self.uuid,
			"name" : self.name,
			"timestamp" : time.time(),
			**payload
		}
		await self.connection.send(json.dumps(packet))

	async def _listen(self):
		async for message in self.connection:
			self.latest = json.loads(message)
			# dispatch the type given by the packet
			await self._dispatch(self.latest["type"]) 
	
	async def _dispatch(self, packetType: str):
		for func in self._listeners.get(packetType, []):
			if inspect.iscoroutinefunction(func):
				await func()
			else:
				raise("Je bent een sukkel want je functie is niet async")

	async def _register(self):
		await self._send("register", foo="bar")
		while 1:
			msg = await self.connection.recv()
			data = json.loads(msg)
			if data["type"] == "regResp":
				break
		# now we know we have received a register response packet
		self.uuid = data['uuid']
		print(self.uuid)

	async def _main(self):
		await self._connect()
		await self._register()
		await self._send("showPacket")
		await self._listen()
	
	def run(self):
		asyncio.run(self._main())

#####################################################################
# Interface

client = Client()

client.url = "ws://127.0.0.1:8000/ws"
client.name = str(randint(0, 10000))

@client.on("showPacket")
async def test():
	print("sent something")
	print(f"We have received {client.latest}")
	

client.run()