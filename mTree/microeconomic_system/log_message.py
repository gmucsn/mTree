from datetime import datetime, timedelta
import time


class LogMessage(object):
    def __init__(self, message_type="", content=None):
        d2 = datetime.now()
        unixtime2 = time.time()
        self.timestamp = unixtime2
        self.message_type = message_type
        self.content = content

    def __str__(self):
        return "<LogMessage Timestamp: {}, Type: {}, Content: {}>".format(self.timestamp, self.message_type,
                                                                self.content)

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