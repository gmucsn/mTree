
class MTreeIntProperty():
    def __init__(self, default_value=None, range=None):
        self.default_value = default_value
        self.range = range


class MTreeBoolProperty():
    def __init__(self, default_value=None):
        self.default_value = default_value


class MTreeRealProperty():
    def __init__(self, default_value=None, range=None):
        self.default_value = default_value
        self.range = range


class MTreeSetProperty():
    def __init__(self, default_value=None, allowed_set=None):
        self.default_value = default_value
        self.allowed_set = allowed_set




