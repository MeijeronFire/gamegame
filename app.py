from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates") # html
app.mount("/static", StaticFiles(directory="static"), name="static") # css

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
	return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI Game", "player_count": 3})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from client: {data}")
            # Echo back a response
            await websocket.send_text(f"Server echo: {data}")
    except Exception as e:
        print("Client disconnected", e)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)