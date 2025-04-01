from fastapi import APIRouter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib
base_router = APIRouter()
import os
from pathlib import Path

from mTree.components.registry import Registry
from mTree.system.actor_system_connector import ActorSystemConnector
from mTree.system.mes_simulation_library import MESSimulationLibrary


templates_folder = pathlib.Path(__file__).parent.joinpath("templates").absolute()

templates = Jinja2Templates(directory=templates_folder)

def examine_directory():
    cwd = os.getcwd()
    p = Path(cwd)
    
    print("DIRECTORY WE ARE LOOKING AT: ", cwd)
    import importlib
    from importlib import import_module

    module = importlib.import_module("mTree.components")

    import glob
    import sys
    from types import ModuleType

    base_module = ModuleType("mTree.components")

    # base_module = ModuleType('cva_mes')
    # sys.modules['cva_mes'] = ModuleType('cva_mes')
    # sys.modules['cva_mes.cva_environment'] = ModuleType('cva_mes.cva_environment')
    # "cva_mes."
    # globals()[module_name] = foo

    modules_imported = []
    module_names = []
    for filename in p.rglob("./mes/*.py"):
    # for filename in glob.iglob("./mes/*.py", recursive=True):
        import_name = os.path.splitext(os.path.basename(filename))[0]

        module_name = "mes." + import_name.partition(".")[0]

        import importlib.util

        # try:
        #    return sys.modules[fullname]
        # except KeyError:
        try:
            spec = importlib.util.spec_from_file_location(module_name, filename)
            # spec = importlib.util.find_spec(fullname)
            # sys.modules[module_name] = ModuleType(module_name)
            module = importlib.util.module_from_spec(spec)
            loader = importlib.util.LazyLoader(spec.loader)
            # Make module with proper locking and get it inserted into sys.modules.
            a = loader.exec_module(module)
            sys.modules[module_name] = module
            # return module

            print(sys.modules[module_name])
        except Exception as e:
            print("An exception,...", e)
            pass
        # foo = importlib.util.module_from_spec(spec)
        # loader = importlib.util.LazyLoader(spec.loader)

        # globals()[module_name] = module
        # print(module)
        # modules_imported.append((module, spec))
        # module_names.append(module)
        # print(foo)
        # base_module

        # spec.loader.exec_module(foo)
        # sys.modules[module_name] = module
        # print(foo)
        # foo.MyClass()
        # module_path = module
        #
        # module_name = os.path.basename(filename)
        # new_module = __import__(module_name, fromlist=[filename])
        # print(new_module)
        # globals()[module_name] = new_module
    # all_my_base_classes = {cls.__name__: cls for cls in base._MyBase.__subclasses__()}

    sys.modules["mes"] = ModuleType("mes")

    import inspect

    target_class = None
    for name, obj in inspect.getmembers(sys.modules["mTree.server"]):
        if inspect.isclass(obj):
            if obj.__name__ == "CVAEnvironment":
                target_class = obj

    # print("SHOULD HAVE LOADED THEM>>>>")
    # print(module_names)
    # print("ABOVE")
    # test = modules_imported[0]
    # for i in modules_imported:
    #     print("\t\tAbout to load: ", i[0])
    #     try:
    #         i[1].loader.exec_module(i[0])
    #     except Exception as e:
    #         print("ISSUE LOADING")
    #         print(e)
    #         print("<<<<<<<<")
    # print(test)
    # spec.loader.exec_module(test)


def find_mes_directories():
    starting_directory = os.getcwd()
    mes_directories = []
    for root, dirs, files in os.walk(starting_directory, topdown=True):
        if "mes" in dirs and "config" in dirs:
            # assume it is a real MES
            mes_directories.append((root, dirs, files))
    return mes_directories


# @base_router.get("/", tags=["users"])
# async def basic(request: Request):
#     # test = examine_directory()
#     known_mes = find_mes_directories()
#     return templates.TemplateResponse("base.html", {"request": request, "message": "asflkjasf", "title": "Page", "mes": known_mes})

@base_router.get("/", tags=["users"])
async def landing(request: Request):
    # if "admin-user" not in session.keys():
    #     return render_template("admin_login.html")
    # else:
    # working_dir = os.getcwd()
    # mes_folders = [
    #     f for f in os.scandir(working_dir) if f.is_dir() and f.name[0] != "."
    # ]
    # component_registry = Registry()
    known_mes = find_mes_directories()
    # return render_template(
    #     "mes_library.html", mes_folders=known_mes#, registry=component_registry
    # )
    return templates.TemplateResponse("mes_library.html", {"request": request, "mes_folders": known_mes})

@base_router.get("/mes_overview", tags=["users"])
async def mes_overview(request: Request, mes_directory:str):
    try:
        # mes_directory = request.args.get("mes_directory")
        readme_file = os.path.join(mes_directory, "README.md")

        readme_file = open(readme_file, "r")
        md_template_string = markdown.markdown(
            readme_file.read(), extensions=["fenced_code"]
        )
    except:
        md_template_string = "Add a README.md"

    # return md_template_string

    return templates.TemplateResponse("mes_overview.html", {"request": request, "title":mes_directory,
        "mes_directory":mes_directory,
        "readme":md_template_string})

@base_router.get("/mes_configurations", tags=["users"])
async def mes_configurations(request: Request, mes_directory:str):
    title = mes_directory + " - Configurations"
    working_dir = os.path.join(mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulations = simulation_library.get_simulations()


    return templates.TemplateResponse("mes_configurations.html", {"request": request, 
        "simulations":simulations,
        "mes_directory":mes_directory,
        "title":title})
    

@base_router.get("/mes_configuration_view", tags=["users"])
async def mes_configuration_view(request: Request, mes_directory:str, configuration:str):
    title = mes_directory + " - " + configuration + " - Configuration"
    working_dir = os.path.join(mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulation = simulation_library.get_simulation_by_filename(configuration)

    return templates.TemplateResponse("mes_configuration_view.html", {"request": request, 
        "simulation":simulation,
        "mes_directory":mes_directory,
        "configuration":configuration,
        "title":title})

@base_router.get("/mes_run_simulation", tags=["users"])
async def mes_run_simulation(request: Request, mes_directory:str, configuration:str):
    component_registry = Registry()

    title = mes_directory + " - " + configuration + " - Configuration"
    working_dir = os.path.join( mes_directory)
    simulation_library = MESSimulationLibrary()
    simulation_library.list_simulation_files_directory(working_dir)
    simulation = simulation_library.get_simulation_by_filename(configuration)

    actor_system = ActorSystemConnector()
    working_dir = os.path.join(mes_directory)
    # actor_system.send_message()
    # actor_system.run_simulation(working_dir, simulation["description"].to_hash())
    actor_system.run_simulation(
        working_dir, configuration, simulation["description"].to_hash()
    )

    # sim_controller = SimulationController()
    # sim_controller.process_configuration(simulation["source_file"])
    return RedirectResponse("/status")
    # return render_template('mes_configuration_view.html',  simulation=simulation, mes_directory=mes_directory, configuration=configuration, title=title)


@base_router.get("/status", tags=["users"])
async def status(request: Request):
    # try:
    title = "Status"
    return templates.TemplateResponse("status.html", {"request": request, 
        "title":title})

    # except TemplateNotFound:
    #    abort(404)
