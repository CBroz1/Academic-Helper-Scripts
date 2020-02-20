# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:29:21

#Purpose: Chromakey videos with neutral grey, watermark videos
#					Turn existing images exported from ppt into videos
#					Concatenate all videos into predetermined sequence

#Caution: a lot here is hardcoded, like video resolution, image names
#				I can't imagine someone will rerun this script, but it incluses
#				ideas for how to script similar processes

if [[ $1 -eq 1 ]] # if arg is 1
	then
	#generate neutral grey
	convert -size 1920x1080 canvas:#808080 gray.png
	#GREEN SCREEN
	for f in Flu_*.mp4
	do
		echo $f
		ffmpeg -hwaccel videotoolbox -i gray1.png -i $f -filter_complex "[1:v] \
		colorkey=0x34d454:0.3:0.15[ckout];[0:v][ckout]overlay[despill];[despill] \
		despill=green[colorspace];[colorspace]format=yuv420p[out]" -map "[out]" \
		./Vid_Chrom/${f%.*}.mkv
	done

	#WATERMARK
	files="./Vid_Chrom/Flu_*.mkv"
	for InFi in $files
	do
		Label=${InFi:16:4}
		# echo $Label
		if [[ $2 -eq 1 ]]
			then
			ffmpeg -loglevel error  -y -i $InFi -vf \
			drawtext='fontfile=/Library/Fonts/Times\ New\ Roman\ Bold.ttf: \
			text='$Label': fontcolor=white: fontsize=32: box=1: boxcolor=black@0.5: \
			boxborderw=5: x=(text_h): y=main_h-(text_h*2)' \
			-codec:a copy ./Vid_Chrom_W/Flu_$Label.mkv
		fi
		Finish='DONE: '; Finish+=$Label ; echo $Finish 
	done
	# ppt img to videos
	vid_dur=4
	array=("0" "1" "2" "3" "4" "5" "6" "7" "8" "9" "Ind1Eng" "Ind1Ger" "Ind2Eng" "Ind2Ger" "Ind3Eng" "Ind3Ger" "Ind4Eng" "Ind4Ger" "Flu1Eng" "Flu1Ger" "Flu2Eng" "Flu2Ger" "Flu3Eng" "Flu3Ger" "Flu4Eng" "Flu4Ger" "Flu5Eng" "Flu5Ger" "Flu6Eng" "Flu6Ger")
	for ((i=1;i<${#array[@]};++i)); do
	    # echo ${array[i]}
	    img=$(printf "./Imgs/Slide%02d.png" $i)
	    echo $img
	    ffmpeg -loglevel error -y -loop 1 -i $img -c:v libx264 -t $vid_dur -pix_fmt yuv420p \
	    ./Vid_Chrom_W/Img_${array[i]}.mkv
	done
	ffmpeg -loglevel error -y -loop 1 -i ./Imgs/gray.png -c:v libx264 -t 2 -pix_fmt \
		yuv420p ./Vid_Chrom_W/Img_Blank.mkv
	# add tone to blank
	ffmpeg -i ./Vid_Chrom_W/Img_Blank.mkv -i ./Imgs/Bottle.aiff -c copy -map 0:v -map 1:a ./Vid_Chrom_W/Img_Blank_Tone.mkv
fi

array2=("Flu_Eng_S" "Flu_Eng_G" "Index_Eng") # "Flu_DGS_G" "Flu_DGS_S" "Index_DGS" "Flu_Ger_G" "Flu_Ger_S" "Index_Ger")
for ((i=0;i<${#array2[@]};++i)); do
	ffmpeg -f concat -safe 0 -i ./text/${array2[i]}.txt -c copy ./Concat/${array2[i]}.mp4
done	




