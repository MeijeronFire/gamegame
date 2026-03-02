from fastapi import FastAPI, WebSocket, Request
from fastapi import WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import cmd
import threading

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
# API endpoints
#

## HTML endpoint
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
	return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Game", "player_count": 3})

## websocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()  # Accept the client connection
	try: # do this until the websocket disconnects unexpectedly
		while 1:	
			try: # do this unless the json is broken
				data = await websocket.receive_text()        # Wait for client message
				msg = json.loads(data)
			except json.JSONDecodeError: # if the json is broken
				await websocket.send_json({"error": "malformed json"})
				continue # wait for the next thingie

			print(f"received {msg["msg"]} at {msg["timestamp"]}")
			# send response
			await websocket.send_json({"lorem": "ipsum"})
	except WebSocketDisconnect:
		print("Client disconnected (normal or abnormal)")

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
	

if __name__ == "__main__":
	console = Console()
	threading.Thread(target=console.cmdloop, daemon=True).start()
	uvicorn.run(app, host="127.0.0.1", port=8000)