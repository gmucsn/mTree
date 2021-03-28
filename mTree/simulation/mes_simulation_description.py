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
        self.mtree_type = "mes_simulation_description"
        self.name = None
        self.id = str(uuid.uuid1())
        self.description = None
        self.environment = None
        self.institution = None
        self.agents = []
        self.properties = {}

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
        print("importing json")
        try:
            # TODO Fix configuration schema validation
            # currently there is an issue on the properties setup...
            #validate(instance=input_json, schema=simulation_description_schema)
            self.configure_from_json(input_json)
        except Exception as e:
            print(e)

    def configure_from_json(self, input_json):
        if "mtree_type" in input_json.keys():
            self.mtree_type = input_json["mtree_type"]
        if "name" in input_json.keys():
            self.name = input_json["name"]
        if "id" in input_json.keys():
            self.id = input_json["id"]
        if "description" in input_json.keys():
            self.description  = input_json["description"]
        if "environment" in input_json.keys():
            print(input_json["environment"])
            self.environment  = input_json["environment"]
        if "institution" in input_json.keys():
            self.institution = input_json["institution"]
        if "agents" in input_json.keys():
            self.agents = input_json["agents"]
        if "properties" in input_json.keys():
            self.properties= input_json["properties"]

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

        temp_dict["environment"] = self.environment
        temp_dict["institution"] = self.institution
        temp_dict["agents"] = self.agents
        temp_dict["properties"] = self.properties
        json_output = json.dumps(temp_dict)
        print(json_output)
    
    def to_hash(self):
        temp_dict = {}
        temp_dict["mtree_type"] = self.mtree_type
        temp_dict["name"] = self.name
        temp_dict["id"] = self.id
        temp_dict["description"] = self.description
        temp_dict["environment"] = self.environment
        temp_dict["institution"] = self.institution
        temp_dict["agents"] = self.agents
        temp_dict["properties"] = self.properties
        return temp_dict
        


