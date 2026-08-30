from flask import render_template


@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)
