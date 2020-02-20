# @Author: CB
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:24:34

#!/bin/bash

#Purpose: Generate average frame, so you can measure where to crop
# 				Then crops all videos depending on user imput
#Caution: user should change crop video numbers

## export frames to average
	for vid in ./orig/*.mpg; do
	 #just first frame:
	 ffmpeg -loglevel panic -i $vid -vframes 1 -f image2 ${vid%%.mpg}.png
	 #all frames - slowwwwww process
	 #process can be sped up by changing image encoding format
	 ffmpeg -i $vid -r 1/1 $filename%05d.png
	done
	mv ./orig/*png ./temp/

## average all first frame
	convert *png -evaluate-sequence mean _Avg.png

## use image editor to check good crop size
	# human work: find crop points of _Avg.png

## crop videos
	# width:height:start crop at x px:start crop at y px
	mkdir -p cropped/
	for i in ./orig/*.mpg; do
	 ffmpeg -loglevel panic -i $i -filter:v \
	 "crop=440:440:283:100" ./cropped/${i##*/} 
	done
