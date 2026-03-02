from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI Game</title>
        </head>
        <body>
            <h1>Welcome to the Game!</h1>
            <p>Connect your WebSocket client to <code>/ws</code> to play.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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