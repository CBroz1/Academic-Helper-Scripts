# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:33:10

#Purpose: Chromakey videos with neutral grey
#Caution: Assumes 1080p res, and mp4 input

mkdir -p Vid_Chrom/ #mkdir if not already exist

#generate neutral grey
convert -size 1920x1080 canvas:#808080 gray.png

#Chromakey
for f in *.mp4
do
	echo $f
	ffmpeg -hwaccel videotoolbox -i gray.png -i $f -filter_complex "[1:v] \
	colorkey=0x34d454:0.3:0.15[ckout];[0:v][ckout]overlay[despill];[despill] \
	despill=green[colorspace];[colorspace]format=yuv420p[out]" -map "[out]" \
	./Vid_Chrom/${f%.*}.mp4
done
