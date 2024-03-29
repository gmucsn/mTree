from jsonschema import validate
import json
import uuid
from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent

simulation_description_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "mtree_type": {
      "type": "string"
    },
    "name": {
      "type": "string"
    },
    "id": {
      "type": "string"
    },
    "description": {
      "type": "string"
    },
    "number_of_runs": {
      "type": "integer"
    },
    "environment": {
      "type": "string"
    },
    "institution": {
      "type": "string"
    },
    "agents": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "agent_name": {
              "type": "string"
            },
            "number": {
              "type": "integer"
            }
          },
          "required": [
            "agent_name",
            "number"
          ]
        }
      ]
    },
    "properties": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "property_name": {
              "type": "string"
            },
            "value": {
              "type": "integer"
            }
          },
          "required": [
            "property_name",
            "value"
          ]
        }
      ]
    }
  },
  "required": [
    "mtree_type",
    "environment",
    "institution",
    "agents"
  ]
}

class MESSimulationDescription():
    def __init__(self, input_json=None, filename=None):
        self.mtree_type = None #"mes_simulation_description"
        self.name = None
        self.id = str(uuid.uuid1())
        self.description = None
        self.number_of_runs = None
        self.environment = None
        self.institution = None
        self.data_logging = None
        self.agents = []
        self.properties = {}
        self.debug = None
        self.log_level = None

        if input_json != None:
            self.import_json(input_json)
        if filename != None:
            self.load_and_import_json(filename)

    def load_and_import_json(self, filename):
        configuration = None
        with open(filename, 'r') as f:
            configuration = json.load(f)
        
        self.import_json(configuration)

    def import_json(self, input_json):
        # try:
            # TODO Fix configuration schema validation
            # currently there is an issue on the properties setup...
            #validate(instance=input_json, schema=simulation_description_schema)
        self.configure_from_json(input_json)
        # except Exception as e:
        #     print(e)

    def configure_from_json(self, input_json):
        if "mtree_type" in input_json.keys():
            self.mtree_type = input_json["mtree_type"]
        if "name" in input_json.keys():
            self.name = input_json["name"]
        if "number_of_runs" in input_json.keys():
            self.number_of_runs = input_json["number_of_runs"]
        if "id" in input_json.keys():
            self.id = input_json["id"]
        if "description" in input_json.keys():
            self.description  = input_json["description"]
        if "environment" in input_json.keys():
            self.environment  = input_json["environment"]
        if "institution" in input_json.keys():
            self.institutions = [{"institution_class": input_json["institution"]}]
        if "institutions" in input_json.keys():
          if isinstance(input_json["institutions"], str):
            self.institutions = [{"institution_class": input_json["institutions"]}]
          else:
            self.institutions = input_json["institutions"]
        if "agents" in input_json.keys():
            self.agents = input_json["agents"]
        if "properties" in input_json.keys():
            self.properties= input_json["properties"]
        if "data_logging" in input_json.keys():
            self.data_logging= input_json["data_logging"]
        if "debug" in input_json.keys():
            if input_json["debug"] == True:
              self.debug = True
        if "log_level" in input_json.keys():
            self.log_level = int(input_json["log_level"])
            


    def set_name(self, name):
        self.name = name

    def set_id(self, id):
        self.id = id

    def set_description(self, description):
        self.description = description


    def set_environment(self, environment_class):
        environment_name = environment_class
        if type(environment_class) == type:
            environment_name = environment_class.__name__
        self.environment = environment_name

    def set_institution(self, institution_class):
        institution_name = institution_class
        if type(institution_class) == type:
            institution_name = institution_class.__name__
        self.institution = institution_name

    def add_agent(self, agent_class, number=1):
        agent_name = agent_class
        if type(agent_class) == type:
            agent_name = agent_class.__name__

        self.agents.append({"agent_name": agent_name, "number": number})

    def to_json(self):
        temp_dict = {}
        temp_dict["mtree_type"] = self.mtree_type
        temp_dict["name"] = self.name
        temp_dict["id"] = self.id
        temp_dict["description"] = self.description
        temp_dict["number_of_runs"] = self.number_of_runs

        temp_dict["environment"] = self.environment
        #temp_dict["institution"] = self.institution
        temp_dict["institutions"] = self.institutions
        temp_dict["agents"] = self.agents
        temp_dict["properties"] = self.properties
        temp_dict["data_logging"] = self.data_logging
        temp_dict["debug"] = self.debug
        temp_dict["log_level"] = self.log_level


        json_output = json.dumps(temp_dict)
    
    def to_hash(self):
        temp_dict = {}
        temp_dict["mtree_type"] = self.mtree_type
        temp_dict["name"] = self.name
        temp_dict["id"] = self.id
        temp_dict["description"] = self.description
        temp_dict["environment"] = self.environment
        #temp_dict["institution"] = self.institution
        temp_dict["institutions"] = self.institutions
        temp_dict["number_of_runs"] = self.number_of_runs
        temp_dict["agents"] = self.agents
        temp_dict["properties"] = self.properties
        temp_dict["data_logging"] = self.data_logging
        temp_dict["debug"] = self.debug
        temp_dict["log_level"] = self.log_level
        
        return temp_dict
        


