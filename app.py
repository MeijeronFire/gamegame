from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates") # html
app.mount("/static", StaticFiles(directory="static"), name="static") # css

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
	return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Game", "player_count": 3})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await websocket.accept()  # Accept the client connection
	while 1:	
		data = await websocket.receive_text()        # Wait for client message
		msg = json.loads(data)
		print(f"received {msg["msg"]} at {msg["timestamp"]}")
		await websocket.send_json({"lorem": "ipsum"})

if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8000)