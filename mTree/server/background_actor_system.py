from mTree.server.actor_system_startup import ActorSystemStartup
import os
import sys
from thespian.actors import *
import time

os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")



def main():
    actor_system = ActorSystemStartup()
    actor_system.startup()

if __name__ == "__main__":
    main()
