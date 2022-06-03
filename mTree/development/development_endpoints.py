from flask import Blueprint, render_template, abort, request, jsonify, redirect, url_for
from flask import session
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from jinja2 import TemplateNotFound
import jinja2
import os
import json
import markdown
import markdown.extensions.fenced_code


# from mTree.components.registry import registry
from mTree.components.registry import Registry
from mTree.simulation.mes_simulation_library import MESSimulationLibrary
from mTree.server.actor_system_connector import ActorSystemConnector
# from mTree.server.configuration_scanner import ConfigurationScanner
# from mTree.runner.server_runner import ServerRunner
# from mTree.server.component_registrar import ComponentRegistrar
# from mTree.server.simulation_controller import SimulationController
from mTree.development.mtree_configuration import MTreeConfiguration


development_area = Blueprint('development_area', __name__, template_folder='templates')

development_area.jinja_loader = jinja2.ChoiceLoader([
    development_area.jinja_loader,
    jinja2.PackageLoader('mTree', 'development/development_templates'),
    #jinja2.PackageLoader(__name__) # in the same folder will search the 'templates' folder
])

@development_area.route('/', defaults={'page': 'index'})
@development_area.route('/<page>')
def show(page):
    if 'admin-user' not in session.keys():
        return render_template('admin_login.html')
    else:
        working_dir = os.getcwd()
        mes_folders = [ f for f in os.scandir(working_dir) if f.is_dir() and f.name[0] != "."]
        component_registry = Registry()
        return render_template('mes_library.html', mes_folders=mes_folders, registry=component_registry)

MTree_configuration = MTreeConfiguration()
ADMIN_PASSOWRD =  MTree_configuration.instance.admin_password

@development_area.route('/admin_login', methods = ['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_credentials = request.form['admin-credentials']
        if admin_credentials == ADMIN_PASSOWRD:
            session['admin-user'] = "ADMIN-USER"
            return redirect("/status")
        else:
            return render_template('admin_login.html', error="Invalid Credentials")    
    

@development_area.route('/subject_runs')
def subject_runs():
    title = "Human Subject Configurations"
    working_dir = os.path.join(os.getcwd())
    mes_directory = working_dir
    simulation_library = MESSimulationLibrary()
    simulation_library.list_human_subject_files_directory(working_dir)
    simulations = simulation_library.get_simulations()

    return render_template('mes_human_subject_configurations.html',  simulations=simulations, mes_directory=mes_directory, title=title) 

@development_area.route('/mes_overview')
def mes_overview():
    try:
        mes_directory = request.args.get('mes_directory')
        readme_file = os.path.join(os.getcwd(), mes_directory, "README.md")
            
        readme_file = open(readme_file, "r")
        md_template_string = markdown.markdown(
            readme_file.read(), extensions=["fenced_code"]
        )
    except:
        md_template_string = "Add a README.md"
    
    #return md_template_string

    return render_template('mes_overview.html', title=mes_directory, mes_directory=mes_directory, readme=md_template_string)
    


@development_area.route('/mes_configurations')
def mes_configurations():
    mes_directory = request.args.get('mes_directory')
    title = mes_directory + " - Configurations"
    working_dir = os.path.join(os.getcwd(), mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulations = simulation_library.get_simulations()

    return render_template('mes_configurations.html',  simulations=simulations, mes_directory=mes_directory, title=title) 

@development_area.route('/mes_configuration_view')
def mes_configuration_view():
    mes_directory = request.args.get('mes_directory')
    configuration = request.args.get('configuration')
    title = mes_directory + " - " + configuration + " - Configuration"
    working_dir = os.path.join(os.getcwd(), mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulation = simulation_library.get_simulation_by_filename(configuration)

    return render_template('mes_configuration_view.html',  simulation=simulation, mes_directory=mes_directory, configuration=configuration, title=title) 

@development_area.route('/mes_human_subject_configuration_view')
def mes_human_subject_configuration_view():
    mes_directory = request.args.get('mes_directory')
    configuration = request.args.get('configuration')
    title = mes_directory + " - " + configuration + " - Configuration"
    working_dir = os.path.join(os.getcwd(), mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulation = simulation_library.get_simulation_by_filename(configuration)

    return render_template('mes_human_subject_configuration_view.html',  simulation=simulation, mes_directory=mes_directory, configuration=configuration, title=title) 



@development_area.route('/status')
def status():
    #try:
        title = "Status"
        return render_template('status.html',  title=title)
        #except TemplateNotFound:
        #    abort(404)

#@development_area.route('/', defaults={'page': 'index'})
@development_area.route('/mes_components')
def mes_components():
    #try:
        mes_directory = request.args.get('mes_directory')
        title = mes_directory + " - Components"
        working_dir = os.path.join(os.getcwd(), mes_directory)
        component_registry = Registry()
        component_registry.clear_contents()
        component_registry.examine_directory(working_dir)
        return render_template('mes_components.html',  title=title, mes_directory=mes_directory, registry=component_registry)
        #except TemplateNotFound:
        #    abort(404)

@development_area.route('/mes_component_view')
def mes_component_view():
    #try:
    mes_directory = request.args.get('mes_directory')
    
    component_registry = Registry()
    component_type = request.args.get('component_type')
    component_name = request.args.get('component_name')
    title = mes_directory + " - " + component_name + " - Component View"
    component_details = component_registry.get_mes_component_details(component_name)
    component_source = component_registry.get_component_source_file(component_name)
    property_list = component_registry.get_mes_component_properties(component_name)
    return render_template('mes_component_view.html', component_details=component_details,
                           component_name=component_name,
                           component_type=component_type,
                           component_source=component_source,
                           property_list=property_list,
                           mes_directory=mes_directory,
                           title=title)


@development_area.route('/system_runs')
def system_runs():
    component_registry = Registry()
    system_runs = component_registry.get_system_runs()
    return render_template('system_runs.html', system_runs=system_runs)

@development_area.route('/view_system_run_output')
def view_system_run_output():
    system_run_log_dir = request.args.get('system_run_log_dir')
    run_code = request.args.get("run_code")
    
    component_registry = Registry()

    if system_run_log_dir is not None:
        system_run_output = component_registry.get_system_run_output(system_run_log_dir)
    else:
        system_run_output = component_registry.get_system_run_output_by_run_code(run_code)

    return render_template('view_system_run_output.html', system_run_output=system_run_output)



@development_area.route('/display_mes_run_configuration')
def display_mes_run_configuration():
    system_run_log_dir = request.args.get('system_run_log_dir')
    component_registry = Registry()
    mes_configuration = component_registry.get_system_run_configuration(system_run_log_dir)
    return render_template('display_mes_run_configuration.html', simulation=mes_configuration)

@development_area.route('/display_mes_run_log')
def display_mes_run_log():
    system_run_log_dir = request.args.get('system_run_log_dir')
    component_registry = Registry()
    mes_run_log = component_registry.get_system_run_log(system_run_log_dir)
    json_run_log = json.dumps(mes_run_log)
    return render_template('display_mes_run_log.html', mes_run_log=json_run_log)

@development_area.route('/display_mes_run_data')
def display_mes_run_data():
    system_run_log_dir = request.args.get('system_run_log_dir')
    component_registry = Registry()
    mes_data_log = component_registry.get_system_data_log(system_run_log_dir)
    json_data_log = json.dumps(mes_data_log)
    return render_template('display_mes_run_data.html', mes_data_log=json_data_log)

@development_area.route('/display_mes_run_sequence_diagram')
def display_mes_run_sequence_diagram():
    system_run_log_dir = request.args.get('system_run_log_dir')
    component_registry = Registry()
    system_run_output = component_registry.get_system_run_output(system_run_log_dir)
    sequence_file = component_registry.read_mes_run_sequence_file(system_run_log_dir)

    return render_template('display_mes_run_sequence_diagram.html', system_run_output=system_run_output,
        sequence_file=sequence_file)


@development_area.route('/mes_results')
def mes_results():
    mes_directory = request.args.get('mes_directory')

    component_registry = Registry()
    system_runs = component_registry.get_system_runs()
    return render_template('system_runs.html', system_runs=system_runs)

    # mes_directory = request.args.get('mes_directory')
    # title = mes_directory + " - Results"
    # log_dir = os.path.join(os.getcwd(), mes_directory, "logs")
    # results_files = []
    # for result_file in os.listdir(log_dir): 
    #     if result_file.endswith(".log") or result_file.endswith(".data"): 
    #         results_files.append(result_file)
    # return render_template('mes_results.html',  results_files=results_files, mes_directory=mes_directory, title=title) 

@development_area.route('/mes_results_view')
def mes_results_view():
    mes_directory = request.args.get('mes_directory')
    results_file = request.args.get('results_file')
    title = mes_directory + " - " + results_file + " - Results"
    data_file = os.path.join(mes_directory, "logs", results_file)
    raw_file_content = ""
    file_content = []
    with open(data_file) as f:
        raw_file_content = f.read()
    for line in raw_file_content.split("\n"):
        try:
            file_content.append((line.split("\t")[0], line.split("\t")[1]))
        except:
            pass
    return render_template('mes_results_viewer.html',  results_file=results_file, mes_directory=mes_directory, title=title, file_content=file_content) 


@development_area.route('/mes_run_human_subject_experiment')
def mes_run_human_subject_experiment():
    mes_directory = request.args.get('mes_directory')
    configuration = request.args.get('configuration')
    component_registry = Registry()


    title = mes_directory + " - " + configuration + " - Configuration"
    working_dir = os.path.join(os.getcwd(), mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulation = simulation_library.get_simulation_by_filename(configuration)

    # actor_system = ActorSystemConnector()
    # working_dir = os.path.join(os.getcwd(), mes_directory)
    # #actor_system.send_message()
    # #actor_system.run_simulation(working_dir, simulation["description"].to_hash())
    # actor_system.run_simulation(working_dir, configuration, simulation["description"].to_hash())


    # sim_controller = SimulationController()
    # sim_controller.process_configuration(simulation["source_file"])

    return redirect(url_for('development_area.human_subject_status', configuration=configuration))
    #return render_template('mes_configuration_view.html',  simulation=simulation, mes_directory=mes_directory, configuration=configuration, title=title) 

@development_area.route('/human_subject_status')
def human_subject_status():
    configuration = request.args.get('configuration')
    title = "Human Subject Status"
    return render_template('human_subject_status.html',  title=title, configuration=configuration)
    

# this endpoint should probably be switched to websockets...
@development_area.route('/mes_run_simulation')
def mes_run_simulation():
    mes_directory = request.args.get('mes_directory')
    configuration = request.args.get('configuration')
    component_registry = Registry()


    title = mes_directory + " - " + configuration + " - Configuration"
    working_dir = os.path.join(os.getcwd(), mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulation = simulation_library.get_simulation_by_filename(configuration)

    actor_system = ActorSystemConnector()
    working_dir = os.path.join(os.getcwd(), mes_directory)
    #actor_system.send_message()
    #actor_system.run_simulation(working_dir, simulation["description"].to_hash())
    actor_system.run_simulation(working_dir, configuration, simulation["description"].to_hash())


    # sim_controller = SimulationController()
    # sim_controller.process_configuration(simulation["source_file"])

    return redirect("/status")
    #return render_template('mes_configuration_view.html',  simulation=simulation, mes_directory=mes_directory, configuration=configuration, title=title) 




        
        
        
    


#@development_area.route('/', defaults={'page': 'index'})
@development_area.route('/component_dashboard')
def component_dashboard(page):
    #try:
        component_registry = Registry()
        print("COMPONENTS AVAILABLE")
        print(component_registry)
        print(component_registry.agent_list())
        return render_template('developer_base.html', registry=component_registry)
        #except TemplateNotFound:
        #    abort(404)



@development_area.route('/component_view')
def component_view():
    #try:
    mes_directory = request.args.get('mes_directory')
    component_registry = Registry()
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
    component_registry = Registry()
    return render_template('simulation_builder.html', registry=component_registry)

@development_area.route('/test_runner')
def test_runner():
    component_registry = Registry()
    return render_template('test_runner.html', registry=component_registry)


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
    component_registry = Registry()
    agent_types = [agent_type for agent_type in component_registry.agent_list()]
    return jsonify(agent_types=agent_types)

@development_area.route('/_generate_simulation_config', methods=['POST'])
def generate_simulation_config():
    clicked = request.form
    print(clicked)

    return jsonify(config_json=clicked)