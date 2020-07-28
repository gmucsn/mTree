from flask import Blueprint, render_template, abort, current_app
from jinja2 import TemplateNotFound
import jinja2
from flask import session
from flask_socketio import emit, join_room, leave_room
#from .. import socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import json


from mTree.components import registry

admin_area = Blueprint('admin_area', __name__, static_folder='build', static_url_path='/')

# admin_area.jinja_loader = jinja2.ChoiceLoader([
#     admin_area.jinja_loader,
#     jinja2.PackageLoader('mTree', 'base/admin_templates'),
#     jinja2.PackageLoader(__name__) # in the same folder will search the 'templates' folder
# ])


@admin_area.route('/')
def index():
    print("ADMIN LOADING")
    return admin_area.send_static_file('index.html')


# @admin_area.route('/', defaults={'page': 'index'})
# @admin_area.route('/<page>')
# def show(page):
#     #try:
#         component_registry = registry.Registry()

#         return render_template('admin_base.html', registry=component_registry)
#         #except TemplateNotFound:
#         #    abort(404)


# @SocketIO.on('chat')
# def handle_my_custom_namespace_event(json):
#     print('received json: ' + str(json))
#     emit('chat', json)

@admin_area.route('/component_view')
def components(page):
    #try:
        component_registry = registry.Registry()

        return render_template('component_view.html', registry=component_registry)