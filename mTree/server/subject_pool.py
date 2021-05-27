from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect,  Namespace
import json

class Subject:
    def __init__(self, sid):
        self.sid = sid




class SubjectPool:
    class __SubjectPool:
        def __init__(self):
            self.subject_pool = {}
            self.flask_outlet = None
            
        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not SubjectPool.instance:
            SubjectPool.instance = SubjectPool.__SubjectPool()

    def register_flask_outlet(self, flask_outlet):
        SubjectPool.instance.flask_outlet = flask_outlet

    def attempt_add(self, sid):
        if sid not in SubjectPool.instance.subject_pool.keys():
            new_subject = Subject(sid)
            SubjectPool.instance.subject_pool[sid] = new_subject
            self.update_subject_pool_emit()
            print("SUBJECT ADDED ", sid)

    def attempt_remove(self, sid):
        if sid in SubjectPool.instance.subject_pool.keys():
            SubjectPool.instance.subject_pool.pop(sid)
            self.update_subject_pool_emit()
            print("SUBJECT REMOVED ", sid)

    def emit(self, message, data):
        response = {"message": message, "data": data}
        SubjectPool.instance.flask_outlet.emit('response', response , namespace='/admin')


    def update_subject_pool_emit(self):
        print("SHOULD EMIT FROM SUBJECT POOL UPDATE")
        self.emit("subject_pool_data", self.get_json())

    def get_json(self):
        subject_ids = []
        subject_hash = {}
        for i in SubjectPool.instance.subject_pool.keys():
            subject_hash[i] = {"sid": i}
            subject_ids.append(i)
        return {"subject_ids": subject_ids, "subject_hash": subject_hash}