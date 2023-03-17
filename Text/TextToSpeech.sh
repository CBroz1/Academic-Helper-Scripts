# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   CBroz1
# @Last Modified time: 2023-03-17 11:20:21

#Purpose: use OSX say command to generate speech from text file
#		Generates timestamped files, opens in Quicktime
#Caution: depends on In.txt input file
#		Generates temporary TTS.aiff and TTS-pro files, then deletes them

wpm=350

for file in $1*.txt
do
	now=`date '+%H%M%S'`;
	base=${file%.*}
	output=${base}_${now}_TTS
	echo $output
	
	cp $file TTS-in.txt
	cat TTS-in.txt | tr -d "\n\r" | sed -e 's/- //g' | sed -e 's/([^()]*)//g' > TTS-pro.txt
	say -v Alex -r $wpm -o TTS.aiff -f TTS-pro.txt
	ffmpeg -loglevel panic -y -i TTS.aiff $output.mp3
	rm -f TTS-in.txt TTS-pro.txt TTS.aiff
	# open -a /Applications/QuickTime\ Player.app/ TTS_$1_$NOW.mp3
done

echo "Done"