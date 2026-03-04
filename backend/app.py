#####################################################################
"""
Accepted protocols:
	Every message must have a:
		- type
		- timestamp
		- own UUID for every request that is not _register_
		- personal name
	Specific queries:
	
	register: registers player
		input:
			name: displayname: (str)
		output:
			type: regResp
			uuid: UUID

	
	getState: returns the current state, i.e. game.state
		input:
		output:
	
	showPacket: returns the packet sent
		input
		output
	
	error: says there is an error
"""
#####################################################################

#
# imports for server
#

# fastapi
from fastapi import FastAPI, WebSocket, Request
from fastapi import WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# admin commands
from backend.console import Console

# actual server 
import uvicorn

#
# utils
#

import json
import threading
from time import sleep

def log(data: dict):
	print(f"""
		Name: {data.get("name")}
		UUID: {data.get("uuid")}
		timestamp: {data.get("timestamp")}
	""")

#
# game modules
#

from game.uber import Uber
uber = Uber()

#
# definitions
#

app = FastAPI()
templates = Jinja2Templates(directory="templates") # html
app.mount("/static", StaticFiles(directory="static"), name="static") # css

#
# mutexes
#

game_lock = threading.Lock()

#
# protocol layer
#

def readMsg(msg: dict) -> dict:
	type = msg["type"]
	match type:
		case "register":
			response = {"type": "regResp",'uuid': uber.genPlayer(msg["name"])}
			print(response)
			return response
		case "getState":
			return {
				"type": "stateResp",
				"data": uber.getState()
			}
		case "showPacket":
			sleep(2)
			print("got showPacket")
			return msg
		case _:
			print("idk what you want")

#
# API endpoints
#

## HTML endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
	return templates.TemplateResponse("index.html", {
			"request": request,
			"title": "FastAPI Game",
			"players" : uber.state["playerNames"]
		})

# TRANSPORT LAYER
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()  # Accept the client connection
	try: # do this until the websocket disconnects unexpectedly
		while 1:	
			try: # do this unless the json is broken
				# read and load message
				data = await websocket.receive_text()
				msg = json.loads(data)
				log(msg)
			except json.JSONDecodeError: # if the json is broken
				await websocket.send_json({"error": "malformed json"})
				continue # wait for the next thingie

			resp = readMsg(msg)
			await websocket.send_json(resp)
	except WebSocketDisconnect:
		print("Client disconnected (normal or abnormal)")

if __name__ == "__main__":
	console = Console(uber)
	threading.Thread(target=console.cmdloop, daemon=True).start()
	uvicorn.run(app, host="127.0.0.1", port=8000)
