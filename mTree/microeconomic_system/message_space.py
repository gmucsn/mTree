from mTree.microeconomic_system.message import Message

class MessageSpace(object):
    def __init__(self, message_type):
        self.message_type = message_type
        self.message_action = None

    @classmethod
    def list_agents(cls):
        message = Message()
        message.set_sender("Environment")  # SPECIAL CASE Environment
        message.set_recipients("Institution")
        message.set_directive("list_agents")
        message.set_payload(None)
        return message

    @classmethod
    def request_agent_list(cls):
        print("AGENT LIST REQUESTED")
        message = Message()
        message.set_sender("Institution")  # SPECIAL CASE Environment
        message.set_recipients("Environment")
        message.set_directive("request_agent_list")
        message.set_payload(None)
        return message

    @classmethod
    def pass_agent_list(cls, agent_list):
        message = Message(sender="Environment", recipients="Institution", directive="agent_list")
        message.set_payload(agent_list)  # TODO include the payoad in the message init
        return message

    @classmethod
    def get_wealths(cls):
        message = Message(sender="Environment", recipients="Agents", directive="get_wealth")  # quicker creation through init
        return message

    def message_type(self):
        return self.message_type

    def message_action(self):
        return self.message_action

    def set_message_action(self, message_action):
        self.message_action = message_action

    @classmethod
    def create_agent(cls, agent_class):
        message = Message()
        message.set_sender("Universe")  # SPECIAL CASE Environment
        message.set_recipients("Environment")
        message.set_directive("create_agent")
        message.set_payload(agent_class)
        return message





