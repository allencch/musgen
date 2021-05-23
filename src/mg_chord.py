from mg_bar import MgBar, mgChord
from mg_time import MgTime
from mg_notes import MgNotes


class MgChord(MgBar):
    """Chord, contains MgNotes"""

    def __init__(self, val=None, chord=None, u=None, l=None):
        self.time = MgTime(u, l)
        self.chord = 'M'
        self.value = 1
        self.rhythm = ()
        self.data = None  # list of MgNotes or MgNote

        if val is None:
            self.data = []
        else:
            if chord is not None and u is not None and l is not None:
                MgBar.setTime(self, u, l)
                self.value = val
                self.chord = chord
                self.process()

    def __repr__(self):
        return self.toString()

    def processTime(self, u, l):
        """Adjust the time
        @param u upper
        @param l lower"""
        MgBar.setTime(self, u, l)
        self.process()

    def processChord(self, value, chord):
        """Process the chord"""
        self.value = value
        self.chord = chord
        self.process()

    def autoAdjust(self):
        for y in self.data:  # x is MgNotes
            for x in y.notes:
                if x.value >= 1 and x.value < 4:
                    x.octave = 1
                else:
                    x.octave = 0

    def ending(self):
        notes = MgNotes()
        notes.set(mgChord(self.value, self.chord))
        notes.setDuration(self.time.upper/self.time.lower)
        self.data = [notes]

    def toString(self):
        text = ""
        for x in self.data:
            text += x.toString()
        return text

    def process(self):
        """Process the chord based on time"""
        notes = MgNotes()
        notes.set(mgChord(self.value, self.chord))

        # Need to based on the rhythm, random rhythm
        self.randRhythm()

        # Based on rhythm generate the note
        self.data = []
        for i in range(len(self.rhythm)):
            notes.setDuration(self.rhythm[i])
            self.data.append(notes.copy())

        # notes.setDuration(self.time.lower)

        #self.data = []
        # for x in range(self.time.upper):
        #   self.data.append(notes.copy())
