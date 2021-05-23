'''Music Generator
Music Generator is a tool to generate music based on chord progression.
This tool is developed to generate the music in the randomness order yet harmonic.
This version intended to generate Lilypond chord.

Concept
=======
Muscial chord properties:
    length
    minor/major
    key

Minor key has the problem, such as Em

Add:
Major7  C,E,G,B
Minor7  C,Eb,G,Bb
'''


import sys

from musgen import Musgen


def main(argv):
    """Main function"""
    options = {'pdf': None,
               'tempo': None,
               'key': None,
               'output': None,
               'instrument': None}
    i = 1  # since 0 is the command itself
    while i < len(argv):
        if argv[i] == "--pdf":
            options['pdf'] = True
        elif argv[i] == "-t":
            options['tempo'] = argv[i+1]
            i += 1
        elif argv[i] == "-k":
            options['key'] = argv[i+1]
            i += 1
        elif argv[i] == "-o":
            options['output'] = argv[i+1]
            i += 1
        elif argv[i] == "--instrument":
            options['instrument'] = argv[i+1]
            i += 1
        i += 1

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
        musgen.randInstrument()  # """

    if options['output']:
        musgen.save(options['output'])
    else:
        print(musgen.lilypond())


if __name__ == '__main__':
    main(sys.argv)

# print mgRandProgression()
