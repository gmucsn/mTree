from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    send_from_directory,
    session,
)
from flask_socketio import (
    Namespace,
    SocketIO,
    close_room,
    disconnect,
    emit,
    join_room,
    leave_room,
    rooms,
)
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
