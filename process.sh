#!/bin/sh
# arguments:
# -f <filename base> = All the filename: .ly, .wave, .midi will based on this
# -o <output type> = Possible value are wav, midi, pdf, mp3, ogg
# -t <tempo> = Tempo
# -k <key>
# --instrument <instrument name>
# eg, ./process.sh -f test -o wav -o midi -o pdf -o mp3 -o ogg, -t 120 -k 5 --instrument 2


TARGET_DIR=/home/allencch/public_html/musgen-temp/
cd $TARGET_DIR
#/usr/bin/python2 ./music-gen.py > $1.ly
#/usr/bin/lilypond $1.ly
#/usr/bin/timidity $1.midi -Ow

#Convert arguments to array for easier access
for ((i=1;i<=$#;i++)) ; do
	ARG[$i]=${!i}
done

for ((i=1;i<=$#;i++)) ; do
	case ${ARG[$i]} in
	-f)
		BASE=${ARG[$i+ 1]}
		((i++))
		;;
	-o)
		case ${ARG[$i+1]} in
		pdf)
			PDF="--pdf"
			((i+=1))
			;;
		wav)
			WAV="-Ow"
			((i+=1))
			;;
		mp3)
			MP3="true"
			((i++))
			;;
		ogg)
			OGG="true"
			;;
		esac
		;;
	-t)
		TEMPO="-t ${ARG[$i+ 1]}"
		((i+=1))
		;;
	-k)
		KEY="-k ${ARG[$i+ 1]}"
		((i+=1))
		;;
	--instrument)
		INSTRUMENT="--instrument ${ARG[$i+1]}"
		((i++))
		;;
	esac
done

#check need wave or not
if [[ -n $MP3 || -n $OGG ]] ; then
	WAV="-Ow"
fi
	
python2 ./music-gen.py $PDF $TEMPO $KEY $INSTRUMENT -o ${BASE}.ly
lilypond ${BASE}.ly

if [[ -n $WAV ]] ; then
	timidity ${WAV} ${BASE}.midi
fi

if [[ -n $MP3 ]] ; then
	sox ${BASE}.wav ${BASE}.mp3
fi

if [[ -n $OGG ]] ; then
	sox ${BASE}.wav ${BASE}.ogg
fi