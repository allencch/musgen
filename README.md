# Musgen (Music Generator)

This is an old project, created in 2011.


## Run script


```
python src/music_gen.py -o output.ly --pdf
```

With `--pdf`, `lilypond` is able to generate the PDF as well.

There are other options, please refer to source code.


## Convert output to music file

Install `lilypond`. Then run

```
lilypond output.ly
```

To play the MIDI file using `timidity`,

```
timidity output.midi
```


# Limitations

* The script uses pre-defined music chord progressions.
* The script only generates time signature 4-4.


# Deprecated notes

Musgen is only the engine.
It uses web interface.
To setup the web interface, the process.sh (or process-cyg.sh) and music-gen.py must be work together. Both files can be put to any folder, then the process.sh will be called by PHP to do the process.
