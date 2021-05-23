import random
from mg_phrase import MG_PROGRESSIONS, MgPhrase
from mg_chord import MgChord
from mg_bar import MgBar


def mgProgressionRule(key, t):
    """Progression rule
    @param t    tuple for the chord
    """
    ret = None
    if key[1] == 'M':
        if t == (1, 'M'):
            ret = [(8, 'M'), (12, 'dim')]

        elif t == (8, 'M') or t == (12, 'dim'):
            ret = [(3, 'm'), (6, 'M')]

        elif t == (3, 'm') or t == (6, 'M'):
            ret = [(10, 'm')]

        elif t == (10, 'm'):
            ret = [(5, 'm'), (8, 'M')]

        elif t == (5, 'm'):
            ret = [(10, 'm'), (8, 'M')]

        ret.append((1, 'M'))

    elif key[1] == 'm':
        if t == (10, 'm'):
            ret = [(5, 'M'), (9, 'dim')]
        elif t == (5, 'M') or t == (9, 'dim'):
            ret = [(12, 'dim'), (3, 'm')]
        elif t == (12, 'dim') or t == (3, 'm'):
            ret = [(6, 'M')]
        elif t == (6, 'M'):
            ret = [(1, 'M')]
        elif t == (1, 'M'):
            ret = [(8, 'M')]
        elif t == (8, 'M'):
            ret = [(3, 'm'), (6, 'M')]

        ret.append((10, 'm'))
    return ret


def mgRandProgression():
    """Get a tuple of (value,chord) tuple randomly"""
    choices = [(1, 'M'), (10, 'm')]  # 2 main key, major or minor
    key = random.choice(choices)
    ret = [key]
    for i in range(7):
        next = mgProgressionRule(key, ret[len(ret)-1])
        chord = random.choice(next)
        ret.append(chord)
    ret.append(key)

    ret.reverse()
    ret.pop()  # remove the last one, because will be replaced with ending
    return tuple(ret)


class MgMusic:
    """Combining treble clef and bass clef, two saffs only"""

    def __init__(self):
        self.treble = MgPhrase()
        self.bass = MgPhrase()
        self.key = (1, 'M')  # C major

    def rand(self):
        choice = random.randint(0, len(MG_PROGRESSIONS)-1)

        #choice = len(MG_PROGRESSIONS)
        MG_PROGRESSIONS.append(mgRandProgression())

        self.key = MG_PROGRESSIONS[choice][0]  # first chord, as the key

        numOfPhrase = random.randint(1, 2)
        for i in range(numOfPhrase):
            treble = MgPhrase()
            bass = MgPhrase()
            treble.randMelody(choice, 4, 4)
            bass.genProgression(choice, 4, 4)
            treble *= 2
            bass *= 2

            self.treble += treble
            self.bass += bass

        """self.treble.randMelody(choice,4,4)
        self.bass.genProgression(choice,4,4)
        self.treble *= 2
        self.bass *= 2 #"""
        ending = MgBar(4, 4)
        ending.randEnd(self.key[0], self.key[1])

        ending2 = MgChord(self.key[0], self.key[1], 4, 4)
        ending2.ending()
        ending2.autoAdjust()

        self.treble.addBar(ending)
        self.bass.addBar(ending2)

        # Add pp to first note of base
        #self.bass.bars[0].data[0].extra = '\p'
