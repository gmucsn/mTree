import json

import jinja2
from flask import Blueprint, abort, render_template, session
# from .. import socketio
from flask_socketio import SocketIO, close_room, disconnect, emit, join_room, leave_room, rooms
from jinja2 import TemplateNotFound
from mTree.components import registry

subject_area = Blueprint("subject_area", __name__, template_folder="templates")

subject_area.jinja_loader = jinja2.ChoiceLoader(
    [
        subject_area.jinja_loader,
        jinja2.PackageLoader("mTree", "server/subject_templates"),
        jinja2.PackageLoader(
            __name__
        ),  # in the same folder will search the 'templates' folder
    ]
)


@subject_area.route("/", defaults={"page": "index"})
@subject_area.route("/<page>")
def show(page):
    # try:
    component_registry = registry.Registry()

    return render_template("subject_base.html", registry=component_registry)
    # except TemplateNotFound:
    #    abort(404)


# @SocketIO.on('chat')
# def handle_my_custom_namespace_event(json):
#     print('received json: ' + str(json))
#     emit('chat', json)
