from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
import jinja2
from flask import session
from flask_socketio import emit, join_room, leave_room
#from .. import socketio
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

import json


from mTree.components import registry
from mTree.simulation.mes_simulation_library import MESSimulationLibrary

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
def component_view():
    #try:
    component_registry = registry.Registry()
    component_type = request.args.get('component_type')
    component_name = request.args.get('component_name')
    component_details = component_registry.get_mes_component_details(component_name)
    component_source = component_registry.get_component_source_file(component_name)
    property_list = component_registry.get_mes_component_properties(component_name)
    return render_template('component_view.html', component_details=component_details,
                           component_name=component_name,
                           component_type=component_type,
                           component_source=component_source,
                           property_list=property_list)

@development_area.route('/simulation_builder')
def simulation_builder():
    component_registry = registry.Registry()
    return render_template('simulation_builder.html', registry=component_registry)

@development_area.route('/simulation_library')
def simulation_library():
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files()

    return render_template('simulation_library.html', simulation_library=simulation_library)

@development_area.route('/simulation_configuration_viewer')
def simulation_configuration_viewer():
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files()
    simulation = None
    for i in simulation_library.get_simulations() :
        if i["description"].id == request.args.get('simulation_configuration_id'):
            simulation = i

    return render_template('simulation_configuration_viewer.html', simulation=simulation)



@development_area.route('/_agent_type_list')
def agent_type_list():
    component_registry = registry.Registry()
    agent_types = [agent_type for agent_type in component_registry.agent_list()]
    return jsonify(agent_types=agent_types)

@development_area.route('/_generate_simulation_config', methods=['POST'])
def generate_simulation_config():
    clicked = request.form
    print(clicked)

    return jsonify(config_json=clicked)