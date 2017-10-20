from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)