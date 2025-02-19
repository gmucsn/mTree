from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, close_room, disconnect, emit, join_room, leave_room, rooms


@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)
