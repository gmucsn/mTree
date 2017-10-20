import datetime


class Recorder:
    """
    Singleton Recorder object
    """
    instance = None

    class __Recorder:
        def __init__(self, args):
            self.file = None  # TODO(@messiest) use class method to set this...
            self.path = "data/"  # TODO(@messiest) think of how this can be set...
            self.logger = open(self.path + "experiment_log.csv", "a")  # TODO(@messiest) How are file names going to be handled?
            self.logger.flush()
            self.write(args)

        def __str__(self):
            return repr(self)

        def write(self, args):
            output = str(datetime.datetime.now())
            for arg in args:
                output += ", {}".format(arg)
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
