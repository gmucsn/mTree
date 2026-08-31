import datetime


class Recorder:
    """
    Singleton Recorder object
    """

    instance = None

    class __Recorder:
        def __init__(self, args):
            self.file = None
            self.path = "data/"
            self.logger = open(self.path + "experiment_log.csv", "a")
            self.logger.flush()
            self.write(args)

        def __str__(self):
            return repr(self)

        def write(self, args):
            output = str(datetime.datetime.now())
            for arg in args:
                output += f", {arg}"
            self.logger.write(output + "\n")
            self.logger.flush()

    def __init__(self, *args):
        if not Recorder.instance:
            Recorder.instance = Recorder.__Recorder(args)
        else:
            Recorder.instance.write(args)

    def set_path(path):
        Recorder.instance.path = path

    def __getattr__(self, name):
        return getattr(self.instance, name)
