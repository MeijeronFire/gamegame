from client import Client
from random import randint

#####################################################################
# Interface

client = Client()

client.url = "ws://127.0.0.1:8000/ws"
#client.name = "Jeffie" #str(randint(0, 10000))
client.name = str(randint(0, 10000))

@client.on("showPacket")
async def test():
	print("sent something")
	print(f"We have received {client.latest}")

@client.on("showPacket")
async def packetsomething():
	await client._send("getState")
	
@client.on("stateResp")
async def stateResp():
	print(client.latest)

client.run()
