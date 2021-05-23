import random
from mg_time import MgTime
from mg_music import MgMusic
from mg_instrument import MgInstrument
from mg_note import MgNote


class Musgen:
    """Music Generator"""
    version = "2.12.3"
    title = "Music Generator Output"
    composer = "Music Generator"
    tempo = 220
    key = 'c'
    bass = '<c e g>2 <c e g>2 <a c e>2 <a c e>2 <f a c>2 <f a c>2 <g b, d>2 <g b, d>2'
    treble = 'e4 g4 e4 c4 | a,4 c4 a,2 | f4 f4 c4 a,4 | g,4 b,4 g2'
    score = ''  # '\\layout {}'
    transpose = 'c'
    instrument = '#"acoustic grand"'  # "acoustic guitar (nylon)"
    instrumentBass = '#"acoustic guitar (nylon)"'

    time = MgTime()

    def __init__(self, options=None):
        if options is not None:
            self.tempo = options['tempo']
            self.transpose = options['transpose']
            self.score = options['score']

        self.music = MgMusic()
        self.music.rand()

    def showLayout(self, value):
        if value == True:
            self.score = '\\layout {}'
        else:
            self.score = ''

    def randTempo(self):
        self.tempo = random.randint(80, 240)

    def setTempo(self, value):
        self.tempo = value

    def randTranspose(self):
        self.transpose = MgNote._names[random.randint(1, 12) - 1]

    def setTranspose(self, value):
        #self.transpose = MgNote(value).toString()
        self.transpose = MgNote._names[value-1]

    def randInstrument(self):
        self.instrument = MgInstrument().rand()

    def setInstrument(self, value):
        self.instrument = MgInstrument().get(value)

    def randMusic(self, value, phase=1):
        """phrase = MgPhrase()
        phrase.genProgression(4,2,2)
        phrase.transpose(2)
        phrase.autoAdjust()
        #phrase += phrase
        self.bass = phrase.toString() #"""

        return self.treble

    def lilypond(self):
        text = """\\version "%(version)s"
\\header {
    title = "%(title)s"
    composer = "%(composer)s"
}

treble = \\transpose c %(transpose)s'' {
    \\set Staff.midiInstrument = %(instrument)s
    \\tempo 4=%(tempo)s

    \\clef treble
    %%\\key %(key)s \\minor
    \\time %(time)s

    %%begin
    {
        %(treble)s
    }

}

bass = \\transpose c %(transpose)s, {
    \\set Staff.midiInstrument = %(instrumentBass)s
    \\clef bass
    %%\\key %(key)s \\minor

    %%\\chordmode
    {
        %(bass)s
    }
}

song = <<
    \\new Staff {
        \\treble
    }
    \\new Staff {
        \\bass
    }
>>

\\score {
    \\song
    \\midi {}
    %(score)s
}
""" % {'version': self.version, 'title': self.title, 'composer': self.composer,
            'tempo': self.tempo, 'key': self.key,
            # 'bass':self.bass,
            # 'treble':self.treble,
            'bass': self.music.bass.toString(),
            'treble': self.music.treble.toString(),
            'score': self.score, 'transpose': self.transpose, 'instrument': self.instrument,
            'instrumentBass': self.instrumentBass, 'time': self.time.toString()}
        return text

    def save(self, filename):
        f = open(filename, "w")
        f.write(self.lilypond())
        f.close()
