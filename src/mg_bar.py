import random
import copy
from mg_time import MgTime
from mg_note import MgNote


def mgChordMajor(value):
    """Return a list of note objects in major"""
    chord = [MgNote(value), MgNote(value) + 4, MgNote(value) + 7]
    return chord


def mgChordMinor(value):
    """Return a list of note objects in minor"""
    chord = [MgNote(value), MgNote(value) + 3, MgNote(value)+7]
    return chord


def mgChordDiminished(value):
    """Return a list of note objects in diminished"""
    chord = [MgNote(value), MgNote(value) + 3, MgNote(value) + 6]
    return chord


def mgChordAugmented(value):
    """Return a list of note objects in augmented"""
    chord = [MgNote(value), MgNote(value) + 4, MgNote(value) + 8]
    return chord


def mgChord(value, chord):
    """Return a list of note based on chord"""
    ret = None
    if chord == 'M':
        ret = mgChordMajor(value)
    elif chord == 'm':
        ret = mgChordMinor(value)
    elif chord == 'dim':
        ret = mgChordDiminished(value)
    elif chord == 'aug':
        ret = mgChordAugmented(value)

    return ret


class MgBar:
    """A music bar, contains list of notes or rest"""
    # data = None #MgNote, MgNotes, or MgRest
    # time = None

    def __init__(self, u=4, l=4):
        self.data = []  # MgNote, MgNotes, or MgRest
        self.time = MgTime(u, l)
        self.rhythm = ()

    def __add__(self, bar):
        for x in bar.copy().data:
            self.data.append(x.copy())
        return self

    def __repr__(self):
        return self.toString()

    def add(self, n):
        self.data.append(n.copy())

    def copy(self):
        return copy.deepcopy(self)

    def transpose(self, value):
        for i in range(len(self.data)):
            self.data[i].transpose(value)

    def setTime(self, u, l):
        self.time.set(u, l)

    def toString(self):
        ret = ''
        for x in self.data:
            ret += x.toString()
        return ret

    def randMelody(self, value, chord):
        """Random rhythm and notes based on time"""
        self.randRhythm()
        self.randNotes(value, chord)

    def randNotes(self, value, chord):
        """Generate random rhythm, based on chord
        It must have rhythm before"""
        aChord = mgChord(value, chord)
        self.data = []
        for i in range(len(self.rhythm)):
            note = random.choice(aChord).copy()
            note.setDuration(self.rhythm[i])
            self.data.append(note)

    def randRhythm(self):
        """Generate random rhythm"""
        rhythm = []
        while self.durationRemain(rhythm) != 0:
            d = self.durationRemain(rhythm)
            if d > 0:
                root = random.randint(1, 3)
                rhythm.append(pow(2, root))
            elif d < 0:
                rhythm.pop()

        self.rhythm = tuple(rhythm)

    def randEnd(self, value, chord):
        aChord = mgChord(value, chord)
        note = random.choice(aChord).copy()
        note.setDuration(self.time.upper / self.time.lower)
        self.data = [note]

    def durationRemain(self, l=None):
        """Get the duration remain, within this bar
        @l  list, values of rhythm
        @return int"""
        if l is None:
            l = self.rhythm
        full = float(self.time.upper)/self.time.lower
        s = 0
        for i in range(len(l)):
            s += 1.0 / l[i]
        return full - s
