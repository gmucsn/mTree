# def test_read_main():
#     ds = DeveloperServer()
#     client = TestClient(ds.app)
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}


# def test_websocket_connection():
#     ds = DeveloperServer()
#     client = TestClient(ds.app)
#     with client.websocket_connect("/admin/actor_system_ws") as admin_websocket:
#         data = admin_websocket.receive_json()
#         assert data == {"msg": "Connected to admin router"}
