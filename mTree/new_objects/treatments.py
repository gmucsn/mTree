import types
import numpy


class Treatments(object):
    treatments = []

    def __init__(self):
        self.treatments = {}
        self.treatment_assignment = None

    def add_treatments(self, treatments):
        for treatment in treatments:
            self.treatments[treatment.name] = treatment

    def set_assignment_method(self, method="balanced"):
        methods = [method for method in dir(Treatments) if isinstance(getattr(Treatments, method), types.FunctionType)]
        if method in methods:  # checks against a list of class methods
            self.treatment_assignment = self.__getattribute__(method)
        else:
            print("Provided object is not a treatment assignment.")

    def balanced(self):
        if Treatments.treatments:  # treatment list not empty
            treatment = Treatments.treatments.pop()
        else:  # treatment list is empty
            Treatments.treatments = list(self.treatments.keys())
            numpy.random.shuffle(Treatments.treatments)
            treatment = Treatments.treatments.pop()
        return treatment

    def random(self):
        if not Treatments.treatments:  # populate treatment list
            Treatments.treatments = list(self.treatments.keys())
            treatment = numpy.random.choice(Treatments.treatments)
        else:
            Treatments.treatments = list(self.treatments.keys())
            treatment = numpy.random.choice(Treatments.treatments)
        return treatment


class Treatment:
    def __init__(self, name):
        self.name = name
        self.value = None


def demo(method="balanced", debug=False):  # Stub code for instantiating treatments
    treatment_a = Treatment('A')
    treatment_b = Treatment('B')
    treatment_c = Treatment('C')

    t_cntrl = Treatments()
    t_cntrl.add_treatments([treatment_a, treatment_b, treatment_c])
    t_cntrl.set_assignment_method(method)

    assignment_counts ={}
    for i in range(10):
        x = t_cntrl.treatment_assignment()
        y = t_cntrl.treatment_assignment()
        z = t_cntrl.treatment_assignment()
        if debug: print("Subject 1: {}, Subject 2: {}, Subject 3: {}".format(x, y, z))

if __name__ == "__main__":
    demo(method="balanced", debug=True)
