class MgNote:
    """A note only"""
    # value = 1
    # octave = 0
    # duration = 4
    _names = ['c', 'cis', 'd', 'dis', 'e', 'f',
              'fis', 'g', 'gis', 'a', 'ais', 'b']

    def __init__(self, value=1, octave=0, duration=4):
        self.value = value
        self.octave = octave
        self.duration = duration

    def __float__(self, value):
        return float(self.value)

    def __repr__(self):
        return self.toString()

    def __add__(self, other):
        self.value = self.value + other
        self.octave += int(float((self.value - 1) / 12))
        self.value = ((self.value - 1) * 10 % 120) / 10 + 1
        return self

    def __sub__(self, other):
        self.value = self.value - other
        self.octave += int(float((self.value - 1) / 12))
        self.value = ((self.value - 1) * 10 % 120) / 10 + 1
        return self

    def copy(self):
        return copy.copy(self)

    def setDuration(self, value):
        self.duration = int(value)

    def getPitch(self):
        """Get the pitch based on value, that is
        convert the octave into value
        @ret int """
        return self.value + self.octave*12

    def setPitch(self, val):
        """Set based on pitch"""
        self.octave = int((val-1)/12)
        self.value = val - (self.octave*12)

    def incOctave(self, val=1):
        """Increase octave"""
        self.octave += val

    def decOctave(self, val=1):
        """Decrease octave"""
        self.octave -= val

    def getName(self):
        text = self._names[int(self.value) - 1]
        if self.octave > 0:
            i = 0
            while i < self.octave:
                text += "'"
                i += 1
        elif self.octave < 0:
            i = 0
            while i > self.octave:
                text += ","
                i -= 1
        return text

    def transpose(self, value):
        self += value

    def toString(self):
        """Include duration"""
        text = self.getName()

        text += str(self.duration) + " "
        return text
