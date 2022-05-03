from mTree.server.actor_system_startup import ActorSystemStartup
import os
import sys
from thespian.actors import *
import time

os.environ['THESPLOG_THRESHOLD'] =  'WARNING'
os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")



def main():
    print("BACKGROUND ACTOR STARTING UP THE ACTOR ENVIRONMENT")
    if len(sys.argv) > 1:
        print("STARTING ACTOR WORLD WITH WEB SOCKET SUPPORT")
        actor_system = ActorSystemStartup(True)
    else:
        actor_system = ActorSystemStartup()
    #actor_system.startup()
    print("BACKGROUND ACTOR STARTUP COMPLETED")


if __name__ == "__main__":
    main()
