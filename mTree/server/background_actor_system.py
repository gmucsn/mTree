from mTree.server.actor_system_startup import ActorSystemStartup
import os
import sys
from thespian.actors import *
import time

os.environ['THESPLOG_THRESHOLD'] =  'WARNING'
os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")



def main():
    if len(sys.argv) > 1:
        actor_system = ActorSystemStartup(True)
    else:
        actor_system = ActorSystemStartup()
    #actor_system.startup()
    

if __name__ == "__main__":
    main()
