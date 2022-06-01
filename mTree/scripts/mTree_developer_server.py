import pyfiglet
import os, signal
from mTree.server.actor_system_startup import ActorSystemStartup
import atexit
import time

# os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
# os.environ['THESPLOG_THRESHOLD'] =  "DEBUG"

#@atexit.register
def goodbye(process=None):
    from thespian.actors import ActorSystem
    print("Shutting down mTree Actor land now...")
    #ActorSystemStartup.shutdown()
    # capabilities = dict([('Admin Port', 19000)])
    # actors = ActorSystem('multiprocTCPBase', capabilities)
    actors = ActorSystem('multiprocTCPBase')
    time.sleep(3)
    actors.shutdown()
    time.sleep(1)
    process.kill()
    process.terminate()
    print("mTree finished shutting down")

#from subprocess import HIGH_PRIORITY_CLASS, DETACHED_PROCESS, CREATE_NO_WINDOW


def launch_background_actor_system():
    # Set Thespian log file location so we can track issues...
    import sys
    from subprocess import Popen, PIPE
    # import subprocess
    # import importlib
    # import importlib.util
    # os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
    # os.environ['THESPLOG_THRESHOLD'] =  "DEBUG"

    print("mTree - Background starting up...")
    background_actor_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "server", "background_actor_system.py")
    process = Popen([sys.executable, background_actor_py, "true"]) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=PIPE, stderr=PIPE)
    atexit.register(goodbye, process=process)

def start_developer_server():
    from mTree.development.development_server import DevelopmentServer#, MTreeController

    ascii_banner = pyfiglet.figlet_format("mTree - Developer Server")
    print(ascii_banner)

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    #SCRIPT_DIR = "/repos/mTree_dev_folder"
    plugins_directory_path = os.path.join(SCRIPT_DIR, 'components')
    # load browser...

    import threading, webbrowser

    port = 5000
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1, lambda: webbrowser.open(url) ).start()
    print("mTree is launching")
    server = DevelopmentServer()
    server.run_server()
    
def main():
    launch_background_actor_system()
    time.sleep(2)
    start_developer_server()


if __name__ == "__main__":
    # Launch the processes
    main()    