import os
import json

class SubjectDirectory:
    class __SubjectDirectory:
        def __init__(self):
            self.subjects = []
            self.experiment_running = False

        def __str__(self):
            return repr(self)



    instance = None

    def __init__(self):
        if not SubjectDirectory.instance:
            SubjectDirectory.instance = SubjectDirectory.__SubjectDirectory()
        
    def update_subjects(self, subject_id, websocket_id):
        found = False
        for index, subject in enumerate(SubjectDirectory.instance.subjects):
            if subject["subject_id"] == subject_id:
                found = True
                SubjectDirectory.instance.subjects[index]["websocket_id"] = websocket_id
                SubjectDirectory.instance.subjects[index]["status"] = "connected"
            
        if not found:
            temp_subject = {}
            temp_subject["subject_id"] = subject_id
            temp_subject["websocket_id"] = websocket_id
            temp_subject["status"] = "connected"
            
            SubjectDirectory.instance.subjects.append(temp_subject)

    def disconnect_subject(self, websocket_id):
        found = False
        for index, subject in enumerate(SubjectDirectory.instance.subjects):
            if subject["websocket_id"] == websocket_id:
                found = True
                SubjectDirectory.instance.subjects[index]["status"] = "disconnected"
        

    def start_experiment(self):
        SubjectDirectory.instance.experiment_running = True

    def experiment_status(self):
        return SubjectDirectory.instance.experiment_running

    def get_subjects_json(self):
        return json.dumps(SubjectDirectory.instance.subjects)

    def get_subjects(self):
        return SubjectDirectory.instance.subjects
