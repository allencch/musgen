#!/usr/bin/python

# Copyright (c) 2011, Allen Choong Chieng Hoon
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the project nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


##
# @file	music-gen.py
# @author	Allen Choong Chieng Hoon
# @date		2011-02-22
# @version	0.2.0
#
# Change log
# 2011-09-20
# Revise for object oriented

'''Music Generator
Music Generator is a tool to generate music based on chord progression.
This tool is developed to generate the music in the randomness order yet harmonic.
This version intended to generate Lilypond chord.

Run in Python 2

Concept
=======
Muscial chord properties:
	length
	minor/major
	key
	
Minor key has the problem, such as Em

Add:
Major7	C,E,G,B
Minor7	C,Eb,G,Bb
'''



import sys, os
import random
import copy
from math import *



"""Progression list"""
MG_PROGRESSIONS = [ ((1,'M'),(6,'M'),(8,'M'),(6,'M')), #C, F, G, F
	((1,'M'),(1,'M'),(6,'M'),(8,'M')), #C, C, F, G
	((1,'M'),(10,'m'),(6,'M'),(8,'M')), #C, Am, F, G
	((10,'m'),(6,'M'),(1,'M'),(5,'M')), #Am, F, C, E
	((1,'M'),(8,'M'),(10,'m'),(5,'m'),(6,'M'),(1,'M'),(3,'m'),(8,'M')),
	((10,'m'),(5,'M'),(6,'M'),(1,'M'),(3,'m'),(10,'m'),(12,'M'),(5,'M')),
	((1,'M'),(3,'m'),(8,'M'),(1,'M')), #C, Dm, G, C
	((1,'M'),(5,'m'),(6,'M'),(8,'M')), #C, Em, F, G
	((1,'M'),(5,'M'),(6,'M'),(3,'M')), #C, E, F, D
	((1,'M'),(11,'M'),(6,'M'),(1,'M')), #C, Bb, F, C
	((1,'M'),(4,'M'),(6,'M'),(1,'M')), #C, Eb, F, C
	((1,'M'),(6,'M'),(4,'M'),(11,'M')), #C, F, Eb, Bb
	((1,'M'),(6,'m'),(11,'M'),(4,'M')), #C, Fm, Bb, Eb
	((1,'M'),(10,'M'),(3,'M'),(8,'M')), #C, A, D, G
	((10,'m'),(6,'M'),(8,'M'),(10,'m')), #Am, F, G, Am
	((1,'M'),(10,'m'),(3,'m'),(8,'M')), #C, Am, Dm, G
	((1,'M'),(11,'M'),(4,'M'),(6,'M')), #C, Bb, Eb, F
	((1,'M'),(4,'M'),(6,'M'),(11,'M')), #C, Eb, F, Bb
	((1,'M'),(8,'M'),(11,'M'),(6,'M')), #C, G, Bb, F
	((1,'M'),(6,'m'),(4,'M'),(11,'M')), #C, Fm, Eb, Bb
	((10,'m'),(1,'M'),(3,'M'),(6,'M')), #Am, C, D, F
]

def mgProgressionRule(key,t):
	"""Progression rule
	@param t	tuple for the chord
	"""
	ret = None
	if key[1] == 'M':
		if t == (1,'M'):
			ret = [(8,'M'),(12,'dim')]
			
		elif t == (8,'M') or t == (12,'dim'):
			ret = [(3,'m'),(6,'M')]
			
		elif t == (3,'m') or t == (6,'M'):
			ret = [(10,'m')]
			
		elif t == (10,'m'):
			ret = [(5,'m'),(8,'M')]
			
		elif t == (5,'m'):
			ret = [(10,'m'),(8,'M')]

		
		ret.append((1,'M'))
		
	elif key[1] == 'm':
		if t == (10,'m'):
			ret = [(5,'M'),(9,'dim')]
		elif t == (5,'M') or t == (9,'dim'):
			ret = [(12,'dim'),(3,'m')]
		elif t == (12,'dim') or t == (3,'m'):
			ret = [(6,'M')]
		elif t == (6,'M'):
			ret = [(1,'M')]
		elif t == (1,'M'):
			ret = [(8,'M')]
		elif t == (8,'M'):
			ret = [(3,'m'),(6,'M')]
			
		ret.append((10,'m'))
	return ret

def mgRandProgression():
	"""Get a tuple of (value,chord) tuple randomly"""
	choices = [(1,'M'),(10,'m')] #2 main key, major or minor
	key = random.choice(choices)
	ret = [key]
	for i in range(7):
		next = mgProgressionRule(key,ret[len(ret)-1])
		chord = random.choice(next)
		ret.append(chord)
	ret.append(key)
		
	ret.reverse() 
	ret.pop() #remove the last one, because will be replaced with ending
	return tuple(ret)
	
	

class MgTime:
	"""Time signature"""
	#upper = 4
	#lower = 4
	
	def __init__(self,u=4,l=4):
		self.upper = u
		self.lower = l
	
	def set(self,u,l):
		self.upper = u
		self.lower = l
		
	def toString(self):
		return str(self.upper) + "/" + str(self.lower)
		
class MgNote:
	"""A note only"""
	#value = 1
	#octave = 0
	#duration = 4
	_names = ['c','cis','d','dis','e','f','fis','g','gis','a','ais','b']
	
	def __init__(self,value=1,octave = 0,duration=4):
		self.value = value
		self.octave = octave
		self.duration = duration
		
	def __float__(self,value):
		return float(self.value)
		
	def __repr__(self):
		return self.toString()
		
	def __add__(self, other):
		self.value = self.value + other
		self.octave += int(float((self.value - 1) / 12))
		self.value = ((self.value - 1) * 10%120) / 10 + 1
		return self
		
	def __sub__(self, other):
		self.value = self.value - other
		self.octave += int(float((self.value -1) / 12))
		self.value = ((self.value - 1)* 10 % 120)/ 10 + 1
		return self
		
	def copy(self):
		return copy.copy(self)
	
	def setDuration(self,value):
		self.duration = int(value)
		
	def getPitch(self):
		"""Get the pitch based on value, that is
		convert the octave into value
		@ret int """
		return self.value + self.octave*12
	
	def setPitch(self,val):
		"""Set based on pitch"""
		self.octave = int((val-1)/12)
		self.value = val - (self.octave*12)
		
	def incOctave(self,val=1):
		"""Increase octave"""
		self.octave += val
		
	def decOctave(self,val=1):
		"""Decrease octave"""
		self.octave -= val
		
	def getName(self):
		text = self._names[self.value -1]
		if self.octave > 0:
			i = 0
			while i < self.octave:
				text += "'"
				i+=1
		elif self.octave < 0:
			i = 0
			while i > self.octave:
				text += ","
				i -= 1
		return text
		
	def transpose(self,value):
		self += value
		
	def toString(self):
		"""Include duration"""
		text = self.getName()
				
		text += str(self.duration) + " "
		return text
		
		
class MgRest(MgNote):
	"""Rest"""
	#duration = 4
	
	def __init__(self,val = 4):
		self.duration = val
		self.value = 1 #will be used in transpose
		
	def __repr__(self):
		return self.toString()
		
	def set(self,val):
		self.duration = val
		
	def copy():
		return copy.copy(self)
		
	def toString(self):
		text = "r" + str(self.duration) + " "
		return text
	
	

class MgInstrument:
	"""Instrument object"""
	_instruments = [ '#"acoustic grand"',
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
	'#"oboe"' ]
	
	def get(self,val):
		return self._instruments[val-1]
		
	def rand(self):
		return random.choice(self._instruments)
		
	
class MgNotes:
	"""Complex notes"""
	#notes = [ MgNote(1) ] #MgNote
	#duration = 4
	
	def __init__(self,n=None):
		if n is None:
			n=MgNote(1)
			
		self.notes = [n] #MgNote
		self.duration = 4
		self.extra = '' #For pp, ff, etc

	
	def __add__(self,val):
		for x in self.notes:
			x += val
		return self
		
	def __sub__(self,val):
		for x in self.notes:
			x -= val
		return self
		
	def __repr__(self):
		return self.toString()
		
	def set(self,l):
		"""Set based on list of MgNote"""
		aList = []
		for x in l:
			aList.append(x.copy())
		self.notes = aList
		
	def add(self,note):
		self.notes.append(note)
		
	def addNotes(self,notes):
		for x in notes.notes:
			self.notes.append(x.copy())
	
	def copy(self):
		return copy.deepcopy(self)
	
	def setDuration(self,val):
		self.duration = int(val)
		
	def down(self):
		"""Move down 1 octave for the highest pitch"""
		self.notes[self._getHighest()].decOctave()
		
	def up(self):
		"""Transpose 1 octave higher"""
		self.notes[self._getLowest()].incOctave()
		
	def transpose(self,value):
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
		
		
		
class MgBar:
	"""A music bar, contains list of notes or rest"""
	#data = None #MgNote, MgNotes, or MgRest
	#time = None
	
	def __init__(self,u=4,l=4):
		self.data = [] #MgNote, MgNotes, or MgRest
		self.time = MgTime(u,l)
		self.rhythm = ()
		
	def __add__(self,bar):
		for x in bar.copy().data:
			self.data.append(x.copy())
		return self
		
		
	def __repr__(self):
		return self.toString()
	
	def add(self,n):
		self.data.append(n.copy())
	
	def copy(self):
		return copy.deepcopy(self)
		
	def transpose(self,value):
		for i in range(len(self.data)):
			self.data[i].transpose(value)
		
	def setTime(self,u,l):
		self.time.set(u,l)
	
	def toString(self):
		ret = ''
		for x in self.data:
			ret += x.toString()
		return ret
		
	def randMelody(self,value,chord):
		"""Random rhythm and notes based on time"""
		self.randRhythm()
		self.randNotes(value,chord)
		
	def randNotes(self,value,chord):
		"""Generate random rhythm, based on chord
		It must have rhythm before"""
		aChord = mgChord(value,chord)
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
				root = random.randint(1,3)
				rhythm.append(pow(2,root))
			elif d < 0:
				rhythm.pop()
		
		self.rhythm = tuple(rhythm)
		
	def randEnd(self,value,chord):
		aChord = mgChord(value,chord)
		note = random.choice(aChord).copy()
		note.setDuration(self.time.upper / self.time.lower)
		self.data = [note]
		
	def durationRemain(self,l=None):
		"""Get the duration remain, within this bar
		@l	list, values of rhythm
		@return int"""
		if l is None:
			l = self.rhythm
		full = float(self.time.upper)/self.time.lower
		s = 0
		for i in range(len(l)):
			s += 1.0 / l[i]
		return full - s
		
		
		
def mgChordMajor(value):
	"""Return a list of note objects in major"""
	chord = [ MgNote(value), MgNote(value) + 4, MgNote(value) + 7]
	return chord
	
def mgChordMinor(value):
	"""Return a list of note objects in minor"""
	chord = [ MgNote(value), MgNote(value) + 3, MgNote(value)+7 ]
	return chord
	
def mgChordDiminished(value):
	"""Return a list of note objects in diminished"""
	chord = [MgNote(value), MgNote(value) + 3, MgNote(value) + 6]
	return chord
	
def mgChordAugmented(value):
	"""Return a list of note objects in augmented"""
	chord = [MgNote(value), MgNote(value) + 4, MgNote(value) + 8]
	return chord
	
def mgChord(value,chord):
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
	
	
class MgChord(MgBar):
	"""Chord, contains MgNotes"""
	def __init__(self,val=None,chord=None,u=None,l=None):
		self.time = MgTime(u,l)
		self.chord = 'M'
		self.value = 1
		self.rhythm = ()
		self.data = None #list of MgNotes or MgNote
		
		if val is None:
			self.data = []
		else:
			if chord is not None and u is not None and l is not None:
				MgBar.setTime(self,u,l)
				self.value = val
				self.chord = chord
				self.process()
				
				
	def __repr__(self):
		return self.toString()
		
	def processTime(self,u,l):
		"""Adjust the time
		@param u upper
		@param l lower"""
		MgBar.setTime(self,u,l)
		self.process()
		
		
	def processChord(self,value,chord):
		"""Process the chord"""
		self.value = value
		self.chord = chord
		self.process()
	
			
	def autoAdjust(self):
		for y in self.data: # x is MgNotes
			for x in y.notes:
				if x.value >= 1 and x.value < 4:
					x.octave = 1
				else:
					x.octave = 0
					
	def ending(self):
		notes = MgNotes()
		notes.set(mgChord(self.value,self.chord))
		notes.setDuration(self.time.upper/self.time.lower)
		self.data = [ notes]
		
		
		
	def toString(self):
		text = ""
		for x in self.data:
			text += x.toString()
		return text
		
	def process(self):
		"""Process the chord based on time"""
		notes = MgNotes()
		notes.set(mgChord(self.value,self.chord))
		
		#Need to based on the rhythm, random rhythm
		self.randRhythm()
		
		#Based on rhythm generate the note
		self.data=[]
		for i in range(len(self.rhythm)):
			notes.setDuration(self.rhythm[i])
			self.data.append(notes.copy())
		
		#notes.setDuration(self.time.lower)
		
		#self.data = []
		#for x in range(self.time.upper):
		#	self.data.append(notes.copy())
		
		
class MgPhrase:
	"""Phrase, contains bars (MgBar or MgChord)"""
	def __init__(self):
		self.bars = [] #contain MgBar or MgChord
		
		
	def __add__(self,phrase):
		for x in phrase.copy().bars:
			self.bars.append(x.copy())
		return self
		
	def __mul__(self,val):
		temp = self.copy()
		for i in range(val-1):
			self.__add__(temp)
		return self
			
	def __repr__(self):
		return self.toString()
		
	def genProgression(self,p,u,l):
		"""Generate chord progression
		@p int, desired progression"""
		progression = MG_PROGRESSIONS[p]
		
		self.bars = []
		for x in progression:
			chord = MgChord(x[0],x[1],u,l)
			chord.autoAdjust()
			self.bars.append(chord)
			
			
	def randMelody(self,p,u,l):
		"""Generate melody, based on chord"""
		progression = MG_PROGRESSIONS[p]
		self.bars = []
		for x in progression:
			bar = MgBar(u,l)
			bar.randMelody(x[0],x[1])
			self.bars.append(bar)
		
			
	def autoAdjust(self):
		for i in range(len(self.bars)):
			self.bars[i].autoAdjust()
		
		
	def copy(self):
		return copy.deepcopy(self)
		
	def addBar(self,bar): #MgBar or MgChord
		self.bars.append(bar.copy())
		
	def addBars(self,bars): # list()
		for x in bars:
			self.bars.append(bar.copy())
			
	def transpose(self,val):
		for i in range(len(self.bars)):
			self.bars[i].transpose(val)
	
	def toString(self):
		text = ''
		for x in self.bars:
			text += x.toString()
		return text
		
		
class MgMusic:
	"""Combining treble clef and bass clef, two saffs only"""
	def __init__(self):
		self.treble = MgPhrase()
		self.bass = MgPhrase()
		self.key = (1,'M') #C major
		
	def rand(self):
		choice = random.randint(0,len(MG_PROGRESSIONS)-1)
		
		#choice = len(MG_PROGRESSIONS)
		MG_PROGRESSIONS.append(mgRandProgression())
		
		self.key = MG_PROGRESSIONS[choice][0] #first chord, as the key
		
		numOfPhrase = random.randint(1,2)
		for i in range(numOfPhrase):
			treble = MgPhrase()
			bass = MgPhrase()
			treble.randMelody(choice,4,4)
			bass.genProgression(choice,4,4)
			treble *= 2
			bass *= 2
			
			self.treble += treble
			self.bass += bass
			
		"""self.treble.randMelody(choice,4,4)
		self.bass.genProgression(choice,4,4)
		self.treble *= 2
		self.bass *= 2 #"""
		ending = MgBar(4,4)
		ending.randEnd(self.key[0],self.key[1])
		
		ending2 = MgChord(self.key[0],self.key[1],4,4)
		ending2.ending()
		ending2.autoAdjust()
		
		self.treble.addBar(ending)
		self.bass.addBar(ending2)
		
		#Add pp to first note of base
		#self.bass.bars[0].data[0].extra = '\p'
		
		


class Musgen:
	"""Music Generator"""
	version = "2.12.3"
	title = "Music Generator Output"
	composer = "Music Generator"
	tempo = 220
	key = 'c'
	bass = '<c e g>2 <c e g>2 <a c e>2 <a c e>2 <f a c>2 <f a c>2 <g b, d>2 <g b, d>2'
	treble = 'e4 g4 e4 c4 | a,4 c4 a,2 | f4 f4 c4 a,4 | g,4 b,4 g2'
	score = '' # '\\layout {}'
	transpose = 'c'
	instrument = '#"acoustic grand"' #"acoustic guitar (nylon)"
	instrumentBass = '#"acoustic guitar (nylon)"'
	
	time = MgTime()
	
	def __init__(self,options=None):
		if options is not None:
			self.tempo = options['tempo']
			self.transpose = options['transpose']
			self.score = options['score']
		
		self.music = MgMusic()
		self.music.rand()
		
	
	def showLayout(self,value):
		if value == True:
			self.score = '\\layout {}'
		else:
			self.score = ''
			
			
	def randTempo(self):
		self.tempo = random.randint(80,240)
		
	def setTempo(self,value):
		self.tempo = value
			
	def randTranspose(self):
		self.transpose = MgNote._names[random.randint(1,12) - 1]
		
	def setTranspose(self,value):
		#self.transpose = MgNote(value).toString()
		self.transpose = MgNote._names[value-1]
		
		
	def randInstrument(self):
		self.instrument = MgInstrument().rand()
			
		
	def setInstrument(self,value):
		self.instrument = MgInstrument().get(value)
			
		
	def randMusic(self,value,phase =1):
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
""" %{'version':self.version, 'title': self.title, 'composer':self.composer,
'tempo':self.tempo, 'key':self.key, 
#'bass':self.bass, 
#'treble':self.treble,
'bass':self.music.bass.toString(),
'treble':self.music.treble.toString(),
'score':self.score,'transpose':self.transpose,'instrument':self.instrument,
'instrumentBass':self.instrumentBass, 'time':self.time.toString()}
		return text;

	def save(self,filename):
		f = open(filename,"w")
		f.write(self.lilypond())
		f.close()
		
		

def main(argv):
	"""Main function"""
	options = {'pdf':None,
		'tempo':None,
		'key':None,
		'output':None,
		'instrument':None}
	i=1 #since 0 is the command itself
	while i < len(argv):
		if argv[i] == "--pdf":
			options['pdf'] = True
		elif argv[i] == "-t":
			options['tempo'] = argv[i+1]
			i+=1
		elif argv[i] == "-k":
			options['key'] = argv[i+1]
			i+=1
		elif argv[i] == "-o":
			options['output'] = argv[i+1]
			i+=1
		elif argv[i] == "--instrument":
			options['instrument'] = argv[i+1]
			i+=1
		i+=1
	
	musgen = Musgen()
	if options['pdf']:
		musgen.showLayout(True)
		
	musgen.randMusic(1)
	
	if options['tempo']:
		musgen.setTempo(int(options['tempo']))
	else:
		musgen.randTempo()
		
	if options['key']:
		musgen.setTranspose(int(options['key']))
	else:
		musgen.randTranspose()
	
	if options['instrument']:
		musgen.setInstrument(int(options['instrument']))
	else:
		musgen.randInstrument() #"""
		
	if options['output']:                       
		musgen.save(options['output'])
	else:
		print musgen.lilypond()
		

main(sys.argv)

#print mgRandProgression()
