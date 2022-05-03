import json
from datetime import datetime, timedelta
import time


class Message(object):
    def __init__(self, sender="", recipients="", directive="", content=None):
        d2 = datetime.now()
        unixtime2 = time.time()
        self.timestamp = unixtime2
        self.sender = sender
        self.recipients = recipients
        self.directive = directive
        self.content = content
        self.short_name = None

    def __str__(self):
        sender = ""
        try:
            if "short_name" in self.content.keys():
                sender = self.content["short_name"]
        except:
            pass

        return "<Message Sender: {}, Recipients: {}, Directive: {}, Content: {}>".format(sender,
                                                                                         self.recipients,
                                                                                         self.directive,
                                                                                         self.content)

    def set_short_name(self, short_name):
        self.short_name = short_name

    def get_short_name(self):
        return self.short_name


    def set_sender(self, sender):
        self.sender = sender

    def get_sender(self):
        return self.sender

    def set_recipients(self, recipients):
        self.recipients = recipients

    def get_recipient(self):
        return self.recipients

    def set_directive(self, directive):
        self.directive = directive

    def get_directive(self):
        return self.directive

    def set_payload(self, content):
        self.content = content

    def set_payload_property(self, payload_field, property):
        try:
            self.content[payload_field] = property
        except:
            pass

    def get_payload_property(self, payload_field):
        return self.content[payload_field]


    def get_payload(self):
        return self.content

    def get_payload_json(self):
        output = ""
        try:
            output = json.dumps(self.content)
        except:
            output = json.dumps(self.content)
        return output