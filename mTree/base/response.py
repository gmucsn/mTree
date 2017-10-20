import json
import os
from jinja2 import Environment, FileSystemLoader


class Response:
    def __init__(self, emitter, app, db, namespace, template_location):
        """
        Initialization of the Response object.
        :param emitter: 
        :param app: 
        :param db: 
        :param namespace: 
        :param template_location: 
        """
        self.emit = emitter
        self.app = app
        #self.db = db
        self.namespace = namespace
        self.template_location = template_location

    #def storeData(self, user, time, probability_A, reward_A, contents_A, probability_B,
    #              reward_B, contents_B, probability_C, reward_C, contents_C, action, box):
    #    a = ExperimentData(user, time, probability_A, reward_A, contents_A, probability_B,
    #                       reward_B, contents_B, probability_C, reward_C, contents_C, action, box)
    #    db.session.add(a)
    #    db.session.commit()

    """
    def logAction(self, level, message):
        if level == "info":
            caller = getframeinfo(stack()[1][0])
            app.logger.info(caller.filename + " -- " + str(caller.lineno) + " -- " + message)
        elif level == "error":
            app.logger.error(message)
        elif level == "warning":
            app.logger.warning(message)
    """

    def set_user_id(self, user_id):
        """
        Associates a unique identifier for the user.
        :param user_id: A unique identifier for the user
        :return: 
        """
        self.emit('willow_action',{
            'data': {"action": "set_user_id", "item": user_id}},
            namespace=self.namespace)

    def show_user(self,  user_id, item_id):  # specifies which user to show the item to.
        # TODO Change show_user() to show(), and show() to show_all()
        """
        Used to display content in the html field marked with the provided id. The content is defined in the html file.
        :param user_id: The user for which the content is displayed
        :param item_id: The id value for the html div or span begin displayed
        :return: 
        """
        self.emit('willow_action', {'data': {"action": "show", "item": item_id}},
                  room=user_id, namespace=self.namespace)

    def show_all(self, item_id):  # why is the user_id passed here? With broadcast=TRUE it should just go to all.
        """
        Used to display the html field marked with the provided id value on all users' screens. 
        :param item_id: The id value for the html div or span begin displayed
        :return: 
        """
        self.emit('willow_action',
             {'data': {"action": "show", "item": item_id}},
                  broadcast=True, namespace=self.namespace)
                  #broadcast=True, room=user_id, namespace=self.namespace)

    def pause(self, state):  # What does this do? Does it work with the admin interface?
        """
        Used to indicate the status of the state to the user.
        :param state: 
        :return: 
        """
        self.emit('willow_action',
             {'data': {"action": "pause", "experiment_state": state}},
             broadcast=True, namespace=self.namespace)

    def add(self, user_id, item_id, html_content, add_instruction="append"):
        # TODO: Change to add_content() for conformity
        """
        Creates a div tag in the html template, and populates it with the provided content.
        :param user_id: The id for the user that the content is being added to 
        :param item_id: The id of the div created where the content is added
        :param html_content: The html content that is added to the template
        :param add_instruction: Determines how the new div is inserted into the template
        :return: 
        """
        self.emit('willow_action',
             {'data': {"action": "add", "new_div_id": item_id, "item": html_content,
                       "add_instruction": add_instruction}},
             room=user_id, namespace=self.namespace)

    def delete_content(self, user_id, item_id):
        # TODO(@skunath) This needs to delete the div, not the content within.
        # This can be done with document.getElementById("my-element").remove();
        """
        Used to remove html content within a div tag. 
        :param user_id: The id for the user that the content is being removed for
        :param item_id: The id of the div from which the content is being removed
        :return: 
        """
        self.emit('willow_action',
             {'data': {"action": "del_content", "div_id": item_id}},
             room=user_id, namespace=self.namespace)

    def get_querystring_callback(self, data):
        print(data)

    def get_querystring_item(self, user_id, querystring_item):
        """
        Used to remove html content within a div tag.
        :param user_id: The id for the user that the content is being removed for
        :param item_id: The id of the div from which the content is being removed
        :return:
        """
        self.emit('willow_action_response',
                  {'data': {"action": "get_parameter", "item": querystring_item}},
                  room=user_id, namespace=self.namespace, callback=self.get_querystring_callback)

    def hide_all(self, item_id):
        """
        Used to hide the html field marked with the provided id value on all users' screens.
        :param item_id: The id value for the html div or span object being hidden
        :return: 
        """
        self.emit('willow_action',
             {'data': {"action": "hide", "item": item_id}},
             broadcast=True, namespace=self.namespace)
             #broadcast=True, room=user_id, namespace=self.namespace)

    def hide_user(self, user_id, item_id):
        """
        Hides content in the html field marked with the provided id.
        :param user_id: The user for which the content is hidden
        :param item_id: The id value for the html div or span begin hidden
        :return:
        """
        self.emit('willow_action',
             {'data': {"action": "hide", "item": item_id}}, room=user_id, namespace=self.namespace)

    def let_all(self, item_id, content):  # TODO think of a more descriptive method name
        """
        Inserts the provided content in the html field marked with the provided id value on all users' screens.
        :param item_id: The id value for the html object
        :param content: What is being inserted to the html item. Treated as a string.
        :return: 
        """
        self.emit('willow_action',
             {'data': {"action": "let", "item": item_id, "content": content}},
             broadcast=True, namespace=self.namespace)

    def let_user(self, user_id, item_id, content):
        """
        Inserts the provided content in the html field marked with the provided id value for a specific user screen. 
        :param user_id: The id value for the html object
        :param item_id: What is being inserted to the html item. Treated as a string.
        :param content: 
        :return: 
        """
        self.emit('willow_action',
                  {'data': {"action": "let", "item": item_id, "content": content}},
                  room=user_id, namespace=self.namespace)

    def set_user(self, user_id, item_id, property_name, property_value):  # What is this method doing???
        """
        :param user_id: 
        :param item_id: 
        :param property_name: 
        :param property_value: 
        :return: 
        """
        self.emit('willow_action',
                  {'data': {"action": "set", "item": item_id, "property_name": property_name, "property_value": property_value}},
                  room=user_id, namespace=self.namespace)

    def set_all(self, item_id, property_name, property_value):
        """
        
        :param item_id: 
        :param property_name: 
        :param property_value: 
        :return: 
        """
        self.emit('willow_action',
                  {'data': {"action": "set", "item": item_id, "property_name": property_name, "property_value": property_value}},
                  broadcast=True, namespace=self.namespace)

    def open_html(self, file):
        """
        Opens html file
        :param file: file path for the html file being opened
        :return: 
        """
        context = {}
        template = Environment(loader=FileSystemLoader(self.template_location or './')).get_template(file).render(context)
        return template

    def alert(self, file, alert_message):  # What does this do?
        """
        
        :param file: 
        :param alert_message: 
        :return: 
        """
        context = {"message" : alert_message}
        template = Environment(loader=FileSystemLoader(self.template_location or './')).get_template(file).render(context)
        return template

    def update_admin_status(self, msg):  # What dis do?
        self.emit('admin_action',
             msg, broadcast=True, namespace="/admin")
