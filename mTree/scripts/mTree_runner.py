import sys, getopt
import json
import importlib
import inspect
import os
import glob

import importlib.util
import sys
import pyfiglet

from mTree.runner.runner import Runner
from mTree.server.actor_system_startup import ActorSystemStartup
import os
import sys
from thespian.actors import *
import time

import atexit
from thespian.actors import *
import time
import sys
from subprocess import Popen, PIPE
import subprocess



@atexit.register
def goodbye():
    print("Shutting down mTree Actor land now...")
    #ActorSystemStartup.shutdown()
    capabilities = dict([('Admin Port', 19000)])
    actors = ActorSystem('multiprocTCPBase', capabilities)
    time.sleep(2)
    actors.shutdown()
    
    print("mTree finished shutting down")


def main():
    # Set Thespian log file location so we can track issues...
    os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
    os.environ['THESPLOG_THRESHOLD'] =  "INFO"

    print("mTree - Background starting up...")
    background_actor_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "server", "background_actor_system.py")
    
    #with open(os.devnull, 'w') as DEVNULL:
    import subprocess
    # creationflags=subprocess.CREATE_NO_WINDOW|subprocess.DETACHED_PROCESS|subprocess.HIGH_PRIORITY_CLASS
    process = Popen([sys.executable, background_actor_py]) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=PIPE, stderr=PIPE)
    #process = subprocess.run([sys.executable, background_actor_py], stdout=DEVNULL, stderr=DEVNULL) #, stdout=PIPE, stderr=PIPE)
    print("Background should have started....")
    launch(sys.argv[1:])

def launch(argv):
    ascii_banner = pyfiglet.figlet_format("mTree")
    print(ascii_banner)
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:m:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('mTreeRunner -i <mtree_configuration_file>')
        sys.exit(2)
    list_simulation = False
    for opt, arg in opts:
        if opt == '-h':
            print('mTreeRunner -i <mtree_configuration_file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-m", "--mcfile"):
            list_simulation = True
            inputfile = arg


    print("mTree Runner")

    actor_system = ActorSystemStartup()
    actor_system.startup()


    mtree_runner = Runner(inputfile, multi_simulation=list_simulation)
    mtree_runner.runner()

if __name__ == "__main__":
    os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
    os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")

    

    main(sys.argv[1:])