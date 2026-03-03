#!/usr/bin/env python3

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
		self._listeners = []
		self._senders = []
	
	def onmessage(self):
		def decorator(func):
			self._listeners.append(func)
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
		...

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
		coroutines = [func() for func in self._listeners + self._senders]
		await asyncio.gather(*coroutines)
	
	def run(self):
		asyncio.run(self._main())

#####################################################################
# Interface

client = Client()

client.url = "ws://127.0.0.1:8000/ws"
client.name = str(randint(0, 10000))

@client.onmessage()
async def test():
	await client._send("showPacket", some="payload")

client.run()