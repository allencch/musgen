import copy
from mg_note import MgNote


class MgNotes:
    """Complex notes"""
    # notes = [ MgNote(1) ] #MgNote
    #duration = 4

    def __init__(self, n=None):
        if n is None:
            n = MgNote(1)

        self.notes = [n]  # MgNote
        self.duration = 4
        self.extra = ''  # For pp, ff, etc

    def __add__(self, val):
        for x in self.notes:
            x += val
        return self

    def __sub__(self, val):
        for x in self.notes:
            x -= val
        return self

    def __repr__(self):
        return self.toString()

    def set(self, l):
        """Set based on list of MgNote"""
        aList = []
        for x in l:
            aList.append(x.copy())
        self.notes = aList

    def add(self, note):
        self.notes.append(note)

    def addNotes(self, notes):
        for x in notes.notes:
            self.notes.append(x.copy())

    def copy(self):
        return copy.deepcopy(self)

    def setDuration(self, val):
        self.duration = int(val)

    def down(self):
        """Move down 1 octave for the highest pitch"""
        self.notes[self._getHighest()].decOctave()

    def up(self):
        """Transpose 1 octave higher"""
        self.notes[self._getLowest()].incOctave()

    def transpose(self, value):
        for i in range(len(self.notes)):
            self.notes[i].transpose(value)

    def toString(self):
        text = '<'
        for x in self.notes:
            text += x.getName() + ' '
        text += '>' + str(self.duration) + self.extra + ' '
        return text

    def _getHighest(self):
        """Get highest note
        @ret int - ith of the list (notes)"""
        rec = None
        thres = -1000
        for i in range(len(self.notes)):
            if self.notes[i].getPitch() > thres:
                thres = self.notes[i].getPitch()
                rec = i
        return rec

    def _getLowest(self):
        """Get lowest note
        @ret int - ith item of the list (notes)"""
        rec = None
        thres = 1000
        for i in range(len(self.notes)):
            if self.notes[i].getPitch() < thres:
                thres = self.notes[i].getPitch()
                rec = i
        return rec
