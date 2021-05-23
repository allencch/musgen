import copy
from mg_bar import MgBar
from mg_chord import MgChord


"""Progression list"""
MG_PROGRESSIONS = [((1, 'M'), (6, 'M'), (8, 'M'), (6, 'M')),  # C, F, G, F
                   ((1, 'M'), (1, 'M'), (6, 'M'), (8, 'M')),  # C, C, F, G
                   ((1, 'M'), (10, 'm'), (6, 'M'), (8, 'M')),  # C, Am, F, G
                   ((10, 'm'), (6, 'M'), (1, 'M'), (5, 'M')),  # Am, F, C, E
                   ((1, 'M'), (8, 'M'), (10, 'm'), (5, 'm'),
                    (6, 'M'), (1, 'M'), (3, 'm'), (8, 'M')),
                   ((10, 'm'), (5, 'M'), (6, 'M'), (1, 'M'),
                    (3, 'm'), (10, 'm'), (12, 'M'), (5, 'M')),
                   ((1, 'M'), (3, 'm'), (8, 'M'), (1, 'M')),  # C, Dm, G, C
                   ((1, 'M'), (5, 'm'), (6, 'M'), (8, 'M')),  # C, Em, F, G
                   ((1, 'M'), (5, 'M'), (6, 'M'), (3, 'M')),  # C, E, F, D
                   ((1, 'M'), (11, 'M'), (6, 'M'), (1, 'M')),  # C, Bb, F, C
                   ((1, 'M'), (4, 'M'), (6, 'M'), (1, 'M')),  # C, Eb, F, C
                   ((1, 'M'), (6, 'M'), (4, 'M'), (11, 'M')),  # C, F, Eb, Bb
                   ((1, 'M'), (6, 'm'), (11, 'M'), (4, 'M')),  # C, Fm, Bb, Eb
                   ((1, 'M'), (10, 'M'), (3, 'M'), (8, 'M')),  # C, A, D, G
                   ((10, 'm'), (6, 'M'), (8, 'M'), (10, 'm')),  # Am, F, G, Am
                   ((1, 'M'), (10, 'm'), (3, 'm'), (8, 'M')),  # C, Am, Dm, G
                   ((1, 'M'), (11, 'M'), (4, 'M'), (6, 'M')),  # C, Bb, Eb, F
                   ((1, 'M'), (4, 'M'), (6, 'M'), (11, 'M')),  # C, Eb, F, Bb
                   ((1, 'M'), (8, 'M'), (11, 'M'), (6, 'M')),  # C, G, Bb, F
                   ((1, 'M'), (6, 'm'), (4, 'M'), (11, 'M')),  # C, Fm, Eb, Bb
                   ((10, 'm'), (1, 'M'), (3, 'M'), (6, 'M')),  # Am, C, D, F
                   ]


class MgPhrase:
    """Phrase, contains bars (MgBar or MgChord)"""

    def __init__(self):
        self.bars = []  # contain MgBar or MgChord

    def __add__(self, phrase):
        for x in phrase.copy().bars:
            self.bars.append(x.copy())
        return self

    def __mul__(self, val):
        temp = self.copy()
        for i in range(val-1):
            self.__add__(temp)
        return self

    def __repr__(self):
        return self.toString()

    def genProgression(self, p, u, l):
        """Generate chord progression
        @p int, desired progression"""
        progression = MG_PROGRESSIONS[p]

        self.bars = []
        for x in progression:
            chord = MgChord(x[0], x[1], u, l)
            chord.autoAdjust()
            self.bars.append(chord)

    def randMelody(self, p, u, l):
        """Generate melody, based on chord"""
        progression = MG_PROGRESSIONS[p]
        self.bars = []
        for x in progression:
            bar = MgBar(u, l)
            bar.randMelody(x[0], x[1])
            self.bars.append(bar)

    def autoAdjust(self):
        for i in range(len(self.bars)):
            self.bars[i].autoAdjust()

    def copy(self):
        return copy.deepcopy(self)

    def addBar(self, bar):  # MgBar or MgChord
        self.bars.append(bar.copy())

    def addBars(self, bars):  # list()
        for x in bars:
            self.bars.append(bar.copy())

    def transpose(self, val):
        for i in range(len(self.bars)):
            self.bars[i].transpose(val)

    def toString(self):
        text = ''
        for x in self.bars:
            text += x.toString()
        return text
