from aiohttp import web
import socketio
from src.chatbot.pipeline import Pipeline


pipe = Pipeline()

sio = socketio.AsyncServer(
    cors_allowed_origins = "*"
)

app = web.Application()

sio.attach(app)

async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect')
async def connect(sid, environ, auth):
    print('connect', sid)

@sio.on('message')
async def print_message(sid, message):
    responses = pipe.run(message, sid)
    print("Socket ID: ", sid)
    for response in responses:
        print("Emit:", response["message"])
        await sio.emit("message",{ "message": response["message"]})
    #print(responses)

app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)