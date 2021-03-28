from flask import Flask, render_template, render_template_string, session, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect,  Namespace
from mTree.server.subject_pool import SubjectPool

class SubjectNamespace(Namespace):
    def __init__(self, namespace=None):
        self.subject_pool = SubjectPool()
        super(Namespace, self).__init__(namespace)

    def on_connect(self):
        self.subject_pool.attempt_add(request.sid)
        
    def on_disconnect(self):
        self.subject_pool.attempt_remove(request.sid)
    

    def get_subject_pool(self):
        return self.subject_pool

        
