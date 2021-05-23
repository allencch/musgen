import random


class MgInstrument:
    """Instrument object"""
    _instruments = ['#"acoustic grand"',
                    '#"harpischord"',
                    '#"clav"',
                    '#"celesta"',
                    '#"piccolo"',
                    '#"marimba"',
                    '#"vibraphone"',
                    '#"dulcimer"',
                    '#"flute"',
                    '#"harmonica"',
                    '#"acoustic guitar (nylon)"',
                    '#"electric piano 1"',
                    '#"electric guitar (jazz)"',
                    '#"electric bass (finger)"',
                    '#"violin"',
                    '#"viola"',
                    '#"cello"',
                    '#"alto sax"',
                    '#"oboe"']

    def get(self, val):
        return self._instruments[val-1]

    def rand(self):
        return random.choice(self._instruments)
