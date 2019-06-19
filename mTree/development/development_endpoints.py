from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
import jinja2
from flask import session
from flask_socketio import emit, join_room, leave_room
#from .. import socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import json


from mTree.components import registry

development_area = Blueprint('development_area', __name__, template_folder='templates')

development_area.jinja_loader = jinja2.ChoiceLoader([
    development_area.jinja_loader,
    jinja2.PackageLoader('mTree', 'development/development_templates'),
    jinja2.PackageLoader(__name__) # in the same folder will search the 'templates' folder
])

@development_area.route('/', defaults={'page': 'index'})
@development_area.route('/<page>')
def show(page):
    #try:
        component_registry = registry.Registry()

        print(component_registry)
        return render_template('developer_base.html', registry=component_registry)
        #except TemplateNotFound:
        #    abort(404)


@development_area.route('/component_view')
def components():
    #try:
    component_registry = registry.Registry()
    component_type = request.args.get('component_type')
    component_name = request.args.get('component_name')
    component_details = component_registry.get_mes_component_details(component_name)
    component_source = component_registry.get_component_source_file(component_name)
    return render_template('component_view.html', component_details=component_details, component_name=component_name,
                           component_type=component_type, component_source=component_source)

    #return render_template('component_view.html', registry=component_registry)