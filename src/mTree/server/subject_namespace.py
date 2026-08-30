from flask import (
    request,
)
from flask_socketio import (
    Namespace,
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
