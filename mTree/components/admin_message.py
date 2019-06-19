
class AdminMessage():
    def __init__(self, json_data):
        self._data = json_data

    def get(self, name):
        return self._data[name]

    def request(self):
        return self.get("request")

