from mTree.development.development_server import DevelopmentServer#, MTreeController
from mTree.server.admin import admin_area
from mTree.microeconomic_system.agent import Agent
import pyfiglet


import importlib
#import inspectf
import os
import glob

import importlib.util
import sys

# For illustrative purposes.
import tokenize
import random, threading, webbrowser
from mTree.server.actor_system_startup import ActorSystemStartup

import atexit
from thespian.actors import *
import time

@atexit.register
def goodbye():
    print("Shutting down mTree Actor land now...")
    #ActorSystemStartup.shutdown()
    capabilities = dict([('Admin Port', 19000)])
    actors = ActorSystem('multiprocTCPBase', capabilities)
    time.sleep(2)
    actors.shutdown()
    
    print("mTree finished shutting down")

import sys
from subprocess import Popen, PIPE
import subprocess
from subprocess import HIGH_PRIORITY_CLASS, DETACHED_PROCESS, CREATE_NO_WINDOW

def main():
    # Set Thespian log file location so we can track issues...
    os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
    os.environ['THESPLOG_THRESHOLD'] =  "INFO"

    print("mTree - Background starting up...")
    background_actor_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "server", "background_actor_system.py")
    
    #with open(os.devnull, 'w') as DEVNULL:
    process = Popen([sys.executable, background_actor_py], creationflags=CREATE_NO_WINDOW|DETACHED_PROCESS|HIGH_PRIORITY_CLASS) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=PIPE, stderr=PIPE)
    #process = subprocess.run([sys.executable, background_actor_py], stdout=DEVNULL, stderr=DEVNULL) #, stdout=PIPE, stderr=PIPE)


    ascii_banner = pyfiglet.figlet_format("mTree - Developer Server")
    print(ascii_banner)

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    #SCRIPT_DIR = "/repos/mTree_dev_folder"
    plugins_directory_path = os.path.join(SCRIPT_DIR, 'components')
    # load browser...

    port = 5000
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1, lambda: webbrowser.open(url) ).start()
    print("mTree is launching")
    server = DevelopmentServer()
    server.run_server()
    


