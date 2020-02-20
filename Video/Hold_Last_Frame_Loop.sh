# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:10:37

# Purpose: extends videos in a directory to desired length
# Cauton: resolution is hard coded into the last ffmpeg line 
#   			See Hold_Last_Frame.sh for info on resolution measurement

TotLength=3 #Total length in seconds

mkdir -p _Finished/
echo "File, CurrentDur, AddingDur, FrameRate" >> _Info.txt

for f in *.m*
do
	#Current duration, Needed additional dur
	CurrentDur="$(ffprobe -v error -show_entries format=duration \
	-of default=noprint_wrappers=1:nokey=1 $f)"
	AdditioDur=$(bc <<< "scale=6;$TotLength-$CurrentDur")
	#get fps as fraction, convert to decimal
	fps_fract="$(ffprobe -v error -select_streams v -print_format \
	flat -show_entries stream=r_frame_rate $f | \
	grep r_frame_rate | cut -b 32- | rev | cut -c 2- | rev)"
	fps_dec="$(bc <<< "scale=6;$fps_fract")"
	#Save info
	echo "${f%.*}, $CurrentDur, $AddingDur, $fps_dec" >> _Info.txt
	#Extend clip
	ffmpeg -f lavfi -i nullsrc=s=720x480:d=$TotLength:r=$fps_fract -i $f \
	-filter_complex "[0:v][1:v]overlay[video]" -map "[video]" -codec:a copy -shortest _Finished/$f
done

