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
    ActorSystem('multiprocQueueBase').shutdown()
    time.sleep(2)




def main():
    # Set Thespian log file location so we can track issues...
    os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
    os.environ['THESPLOG_THRESHOLD'] =  "DEBUG"

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
    


