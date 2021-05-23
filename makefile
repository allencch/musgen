all: output.midi

test:
	python src/music_gen.py -o output.ly
	lilypond output.ly
	timidity output.midi

test_pdf:
	python src/music_gen.py -o output.ly --pdf
	lilypond output.ly
	timidity output.midi


output.midi: output.ly
	lilypond $?

output.ly: src/music_gen.py
	python src/music_gen.py > output.ly
