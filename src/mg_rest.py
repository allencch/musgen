import copy
from mg_note import MgNote


class MgRest(MgNote):
    """Rest"""
    #duration = 4

    def __init__(self, val=4):
        self.duration = val
        self.value = 1  # will be used in transpose

    def __repr__(self):
        return self.toString()

    def set(self, val):
        self.duration = val

    def copy():
        return copy.copy(self)

    def toString(self):
        text = "r" + str(self.duration) + " "
        return text
