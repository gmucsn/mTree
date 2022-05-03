import json
from datetime import datetime, timedelta
import time


class AdminMessage(object):
    def __init__(self, request=None, response=None, payload=None):
        d2 = datetime.now()
        unixtime2 = time.time()
        self.timestamp = unixtime2
        self.request = request
        self.payload = payload
        
        self.response = response

    def get_response(self):
        return self.response
    
    def get_request(self):
        return self.request

    def get_payload(self):
        return self.payload

    def set_payload(self, payload):
        self.payload = payload

    def __str__(self):
        return "<AdminMessage Request: {}, Response: {}, Payload: {}>".format(self.request, self.response, self.payload)

    