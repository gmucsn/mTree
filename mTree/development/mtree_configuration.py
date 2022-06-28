import os
import json

class MTreeConfiguration:
    class __MTreeConfiguration:
        def __init__(self):
            self.admin_password = "adminmtree"
            self.subject_ids = ["A1234"]
        def __str__(self):
            return repr(self)



    instance = None

    def __init__(self):
        if not MTreeConfiguration.instance:
            MTreeConfiguration.instance = MTreeConfiguration.__MTreeConfiguration()
            
            try:
                self.read_config_file()
            except:
                pass
        
    def read_config_file(self):
        # read configuration file...
        configuration = None
        cwd = os.getcwd()
        config_file_path = os.path.join(cwd, "mtree_config.json")
        with open(config_file_path, "r") as config_in:
            configuration = json.load(config_in)

        MTreeConfiguration.instance.admin_password = configuration["admin_password"]
        MTreeConfiguration.instance.subject_ids.extend(configuration["subject_ids"])
    