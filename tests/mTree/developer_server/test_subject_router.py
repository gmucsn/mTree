import asyncio
import json

import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

from mTree.developer_server.developer_server import DeveloperServer

# def test_read_main():
#     ds = DeveloperServer()
#     client = TestClient(ds.app)
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}



@pytest.mark.anyio
async def test_multiple_concurrent_websockets():
    # Initialize the synchronous test client
    ds = DeveloperServer()
    client = TestClient(ds.app)
    subject_id = 1
    # 1. Connect Client A and Client B manually (non-blocking)
    # Using the context manager's __enter__ directly allows keeping connections alive
    ctx_a = client.websocket_connect("/admin/experiment_ws")
    # ctx_c = client.websocket_connect("/admin/experiment_ws")
    ctx_b = client.websocket_connect("/subject/experiment_ws/{subject_id}")
    
    ctx_d = client.websocket_connect("/subject/turbo-stream/{subject_id}")
    
    ws_a = ctx_a.__enter__()
    # ws_c = ctx_c.__enter__()
    ws_b = ctx_b.__enter__()
    # ws_d = ctx_d.__enter__()

    try:
        # 2. Define concurrent behaviors for each client
        async def client_a_behavior():
            # Send a message from Client A
            ws_a.send_text("Hello from Client A")
            
            # Client A should receive its own broadcasted message
            data_a = ws_a.receive_text()
            assert json.loads(data_a) == {"msg":"Connected to admin router"}

        async def client_b_behavior():
            # Client B should receive Client A's broadcasted message concurrently
            data_b = ws_b.receive_text()
            assert json.loads(data_b) == {"msg":"Connected to subject router"}


        # 3. Execute behaviors simultaneously in the event loop
        await asyncio.gather(
            client_a_behavior(),
            client_b_behavior()
        )

    finally:
        # 4. Safely clean up and tear down both connections
        ctx_a.__exit__(None, None, None)
        ctx_b.__exit__(None, None, None)

# def test_websocket():
#     ds = DeveloperServer()
#     client = TestClient(ds.app)
#     subject_id = 1
#     with client.websocket_connect("/admin/actor_system_ws") as admin_websocket:            
#         with client.websocket_connect("/subject/experiment_ws/{subject_id}") as websocket:
#             data = websocket.receive_json()
#             assert data == {"msg": "Hello WebSocket"}

