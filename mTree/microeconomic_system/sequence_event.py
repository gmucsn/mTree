from datetime import datetime, timedelta
import time


class SequenceEvent(object):
    def __init__(self, timestamp, sender, receiver, directive):
        self.timestamp = timestamp
        self.sender = sender
        self.receiver = receiver
        self.directive = directive
        
    def __str__(self):
        return "<SequenceEvent Timestamp: {}, Sender: {}, Receiver: {}, Directive: {}>".format(self.timestamp, 
                                                            self.sender,
                                                            self.receiver,
                                                            self.directive)

    def set_message_type(self, message_type):
        self.message_type = message_type

    def get_message_type(self):
        return self.message_type

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_timestamp(self):
        return self.timestamp

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content