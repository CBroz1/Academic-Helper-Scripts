# @Author: CB
# @Date:   2017-05-19 21:56:16
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:14:04

#!/bin/bash

# purpose: take input video, generate png of last frame
# caution: assumes .mov format - change $of definition to actual format
# caution: loglevel panic keeps ffmpeg mostly silent. 
# 					see following for more verbose options: ffmpeg.org/ffmpeg.html

fn="$1" 														#input file
of=`echo Last_$1 | sed s/mov/png/`  #output file is not MOV, is PNG

## Measure last frame number
lf=`ffprobe -loglevel panic -show_streams "$fn" 2> /dev/null | grep nb_frames | head -1 | cut -d \= -f 2`
let "lf = $lf - 1" # actual last frame is ffprobe's measurement minus 1

## Generate png
ffmpeg -loglevel panic -i $fn -vf select=\'eq\(n,$lf\) -vframes 1 $of

## generate 1s clip of output png
#ffmpeg -loglevel panic -loop 1 -i $of -c:v libx264 -t 1 -pix_fmt yuv420p Ext_$1