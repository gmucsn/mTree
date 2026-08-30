"""
Small utility file to examine websocket connections to the server.
"""

import websocket

ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:8000/admin/actor_system_ws")
ws.send("Hello, Server")
# 19
while True:
    print(ws.recv())
# ?Hello, Server
# ws.close()
