import socketio

sio=socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')

@sio.on("connect")
async def connect(sid, env):
    print("New Client Connected to This id :"+" "+str(sid))

@sio.on("disconnect")
async def disconnect(sid):
    print("Client Disconnected: "+" "+str(sid))