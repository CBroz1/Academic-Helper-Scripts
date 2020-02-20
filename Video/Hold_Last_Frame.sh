# @Author: Chris Brozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:11:02

# This script take a video specified by $mov and holds the last frame
# for $HoldDur seconds. Please install ffmpeg before running.
# For OSX, homebrew makes ffmpeg install easy.

mov="mov.mp4" #video filename
HoldDur=1.0 #duration of hold in s.ms

MovPlusFrame="${mov%.*}_Held.${mov##*.}" #extended filename_Held.ext

## GetInfo about video
# frames per second, fraction
fps_fract="$(ffprobe -v error -select_streams v -print_format \
	flat -show_entries stream=r_frame_rate $mov | \
	grep r_frame_rate | cut -b 32- | rev | cut -c 2- | rev)"
# frames per secondd as a decimal
fps_dec="$(bc <<< "scale=6;$fps_fract")"
# Resolution
MovRes=$(ffprobe -v error -select_streams v:0 -show_entries \
	stream=width,height -of csv=s=x:p=0 $mov)
# Duration
dur=$(ffmpeg -i $mov 2>&1 | grep "Duration"| cut -d ' ' -f 4 | sed s/,// )
durSec=$(echo $dur | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')
FullTime="$(bc <<< "$durSec + $HoldDur")"

## Make the extended video
ffmpeg -y -loglevel error -f lavfi -i \
	nullsrc=s=$MovRes:d=$FullTime:r=$fps_fract \
	-i $mov -filter_complex "[0:v][1:v]overlay[video]" \
	-map "[video]" -codec:a copy -shortest $MovPlusFrame

# report durations for all files in folder
# Serves as a sanity check, because different measurement tools disagree
#		Psyscope, at time of first writing, was giviing us diff numbers
for file in *.${mov##*.}
do
	# echo "${file} duration:" 
	du=$(ffmpeg -i $file 2>&1 | grep "Duration"| \
		cut -d ' ' -f 4 | sed s/,// )
	echo $du $file 
done

#---------------------------------------------------------------#

## Old version of file
## saved last frame as png, then made a video
## THEN made a vid from png and used ffmpeg -concat List.txt

# LastFramePic="${mov%.*}_LaFr.png"
# LastFrameHold="${mov%.*}_Still.${mov##*.}"
# LastFrame=$(
# 	ffprobe -v error -count_frames -select_streams v:0 \
# 	-show_entries stream=nb_read_frames -of \
# 	default=nokey=1:noprint_wrappers=1 $mov) 
# LastFrame=$((LastFrame-1)) ## frame number un-0-indexed
# ffmpeg -y -loglevel error -i $mov -vf \
# 	"select='eq(n,$LastFrame)'" -vframes 1 \
# 	$LastFramePic

# ffmpeg -y -loglevel error -loop 1 -i $LastFramePic \
# 	-c:v libx264 -t $HoldDur -pix_fmt yuv420p $LastFrameHold

# echo "file '$mov'" > List.txt
# echo "file '$LastFrameHold'" >> List.txt

# # ffmpeg -y -safe 0 -f concat -i List.txt -c copy $MovPlusFrame
# ffmpeg -y -safe 0 -f concat -segment_time_metadata 1 -i List.txt \
# 	-vf select=concatdec_select \
# 	-af aselect=concatdec_select,aresample=async=1 $MovPlusFrame