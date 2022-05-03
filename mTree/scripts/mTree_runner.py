import sys
import os
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

import argparse


@atexit.register
def goodbye():
    #print("Shutting down mTree Actor land now...")
    #ActorSystemStartup.shutdown()
    capabilities = dict([('Admin Port', 19000)])
    actors = ActorSystem('multiprocTCPBase') #, capabilities)
    time.sleep(2)
    actors.shutdown()
    
    #print("mTree finished shutting down")


def main():
    # Set Thespian log file location so we can track issues...
    os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
    # TODO Fix and make this selectable from the command line
    os.environ['THESPLOG_THRESHOLD'] =  "DEBUG"

    background_actor_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "server", "background_actor_system.py")
    
    #with open(os.devnull, 'w') as DEVNULL:
    import subprocess
    # creationflags=subprocess.CREATE_NO_WINDOW|subprocess.DETACHED_PROCESS|subprocess.HIGH_PRIORITY_CLASS
    process = Popen([sys.executable, background_actor_py], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, stdout=PIPE, stderr=PIPE)
    #process = subprocess.run([sys.executable, background_actor_py], stdout=DEVNULL, stderr=DEVNULL) #, stdout=PIPE, stderr=PIPE)
    time.sleep(3)
    launch() #sys.argv[1:])

def launch():
    ascii_banner = pyfiglet.figlet_format("mTree  - Runner")
    print(ascii_banner)
    inputfile = ''
    outputfile = ''
    # try:
    #     opts, args = getopt.getopt(argv,"hi:m:o:",["ifile=","ofile="])
    # except getopt.GetoptError:
    #     print('mTreeRunner -i <mtree_configuration_file>')
    #     sys.exit(2)
    list_simulation = False
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print('mTreeRunner -i <mtree_configuration_file>')
    #         sys.exit()
    #     elif opt in ("-i", "--ifile"):
    #         inputfile = arg
    #     elif opt in ("-m", "--mcfile"):
    #         list_simulation = True
    #         inputfile = arg


    #print("mTree Runner")

    # actor_system = ActorSystemStartup()
    # actor_system.startup()

    mtree_runner = Runner(os.getcwd())
    mtree_runner.runner()




if __name__ == "__main__":
    os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
    os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")

    parser = argparse.ArgumentParser(description='mTree Runner')
    args = parser.parse_args()

    main() #sys.argv[1:])

#     print("ALSFJKHASKLJFHALKSJDFLKAJS")
#     os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
#     os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
#     print("!#@#")
#     parser = argparse.ArgumentParser(add_help=False, description='mTree Runner')
#     parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
#                     help='Show information on mTree Runner.')
#     args = parser.parse_args()
    
#     print(args)
#     print(args.accumulate(args.integers))
#     print("^^^^^")
    

#     #main(sys.argv[1:])