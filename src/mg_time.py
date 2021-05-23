class MgTime:
    """Time signature"""
    # upper = 4
    # lower = 4

    def __init__(self, u=4, l=4):
        self.upper = u
        self.lower = l

    def set(self, u, l):
        self.upper = u
        self.lower = l

    def toString(self):
        return str(self.upper) + "/" + str(self.lower)
