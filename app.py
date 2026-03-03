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


#
# imports for server
#

from fastapi import FastAPI, WebSocket, Request
from fastapi import WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

#
# utils
#

import json
import cmd
import threading

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
# console_print_lock = threading.Lock()
# def safe_print(*args, **kwargs):
# 	with console_print_lock:
# 		print(*args, **kwargs)

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
			return uber.getState()
		case "showPacket":
			return msg
		case _:
			print("idk what you want")

#
# console
#

class Console(cmd.Cmd):
	intro = "Lorem Ipsum Dolor Sit Amet"
	prompt = "[anker] - "

	def do_hello(self, arg):
		"""
		usage: hello <name>

		name: person to greet
		"""
		print(f"Hello {arg}")
	
	def do_printstate(self, arg):
		"""
		usage: printstate
		
		prints current state of game
		"""
		print(f"{uber.state}")
	
	def do_printplayerdata(self, arg):
		"""
		usage: printstate
		
		prints current state of game
		"""
		print(f"{uber.playerData}")

def log(data: dict):
	print(f"""
		Name: {data.get("name")}
		UUID: {data.get("uuid")}
		timestamp: {data.get("timestamp")}
	""")

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
	console = Console()
	threading.Thread(target=console.cmdloop, daemon=True).start()
	uvicorn.run(app, host="127.0.0.1", port=8000)
