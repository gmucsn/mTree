from mTree.server.actor_system_startup import ActorSystemStartup
import os

os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")
os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'


actor_system = ActorSystemStartup()
actor_system.load_base_mes()