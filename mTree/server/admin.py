from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import jinja2
from flask import session
from flask_socketio import emit, join_room, leave_room
#from .. import socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import json


from mTree.components import registry

admin_area = Blueprint('admin_area', __name__, template_folder='templates')

admin_area.jinja_loader = jinja2.ChoiceLoader([
    admin_area.jinja_loader,
    jinja2.PackageLoader('mTree', 'base/admin_templates'),
    jinja2.PackageLoader(__name__) # in the same folder will search the 'templates' folder
])

@admin_area.route('/', defaults={'page': 'index'})
@admin_area.route('/<page>')
def show(page):
    #try:
        component_registry = registry.Registry()

        return render_template('admin_base.html', registry=component_registry)
        #except TemplateNotFound:
        #    abort(404)


@admin_area.route('/component_view')
def components(page):
    #try:
        component_registry = registry.Registry()

        return render_template('component_view.html', registry=component_registry)