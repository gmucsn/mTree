from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import jinja2
from flask import session
from flask_socketio import emit, join_room, leave_room
#from .. import socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import json


from mTree.components import registry

subject_area = Blueprint('subject_area', __name__, template_folder='templates')

subject_area.jinja_loader = jinja2.ChoiceLoader([
    subject_area.jinja_loader,
    jinja2.PackageLoader('mTree', 'server/subject_templates'),
    jinja2.PackageLoader(__name__) # in the same folder will search the 'templates' folder
])

@subject_area.route('/', defaults={'page': 'index'})
@subject_area.route('/<page>')
def show(page):
    #try:
        component_registry = registry.Registry()

        return render_template('subject_base.html', registry=component_registry)
        #except TemplateNotFound:
        #    abort(404)


# @SocketIO.on('chat')
# def handle_my_custom_namespace_event(json):
#     print('received json: ' + str(json))
#     emit('chat', json)
