class Message(object):
    def __init__(self, sender="", recipients="", directive="", content=None):
        self.sender = sender
        self.recipients = recipients
        self.directive = directive
        self.content = content

    def __str__(self):
        return "<Message Sender: {}, Recipients: {}, Directive: {}, Content: {}>".format(self.sender,
                                                                                         self.recipients,
                                                                                         self.directive,
                                                                                         self.content)

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

    def get_payload(self):
        return self.content