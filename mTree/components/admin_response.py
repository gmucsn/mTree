
class AdminResponse():
    def __init__(self, json_data):
        self._data = json_data

    def getJson(self):
        return self._data

    def get(self, name):
        return self._data[name]

