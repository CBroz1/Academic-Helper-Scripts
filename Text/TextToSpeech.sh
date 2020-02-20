# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:48:30

#Purpose: use OSX say command to generate speech from text file
#		Generates timestamped files, opens in Quicktime
#Caution: depends on In.txt input file
#		Generates temporary TTS.aiff and TTS-pro files, then deletes them


wpm=450 #words per min 
# wpm=350
in="TTS.txt" #input
out="TTS.aiff" #out file

NOW=`date '+%H%M%S'`;
echo $NOW

cat $in | tr -d "\n\r" | sed -e 's/- //g' | sed -e 's/([^()]*)//g' > TTS-pro.txt


say -v Alex -r $wpm -o $out -f TTS-pro.txt
ffmpeg -y -i $out TTS_$1_$NOW.mp3; rm TTS.aiff; rm TTS-pro.txt
open -a /Applications/QuickTime\ Player.app/ TTS_$1_$NOW.mp3

