# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   Chris
# @Last Modified time: 2017-09-12 01:17:29

#Linux is different in 5vs6 in LAST_num definition
#Linux is different in suffix on cp command
#Mac can handle numbers in filename, Linux has trouble

Sizing='50%' #Size of gifs compared to size of video, as percentage

mkdir -p zFrames #if does not exist, make folder 'zFrames'
touch _Info.txt  #if does not exist, make _Info file

for f in *.m*    #For file in current directory that fits description (currently, extension starts with m)
do
	echo ${f%.*} #print file name, without extension, to terminal
	ffmpeg -loglevel error -i $f -qscale:v 2 -vf fps=25 zFrames/${f%.*}-%03d.jpg
	#save jpgs from video
	#log only errors in this process, input as file, best image quality (2), 25 frames per second
	#save images in zFrames folder ordered sequentially, 001
	LAST_fi=`exec ls zFrames/*jpg | sed 's/\([0-9][0-9][0-9]\+\).*/\1/g' | sort -n | tail -1`
	#find last file of the recently created jpgs
	LAST_num=$( printf "%.0f" ${LAST_fi:${#f}+5:4} )
	#store last file as number
	echo $LAST_fi
	#echo last file to terminal
	echo "${f%.*}, $LAST_num" >> _Info.txt
	#add both file name and number of frames to _Info.txt file
	for i in `seq $((LAST_num+1)) $((LAST_num+13))`; do #for numbers Last_num+1 to +13, do
		cp $LAST_fi zFrames/${f%.*}-$(printf "%03d" $i).jpg #Copy paste, extending gif length by ~.5sec
	done
	convert -delay 4 -loop 0 zFrames/${f%.*}*.jpg -resize $Sizing +repage -layers optimize ${f%.*}.gif
	#make gif. delay is 100/fps. do not loop. Pull images from zFrames folder. resize as percentage
	rm zFrames/${f%.*}*.jpg
	#Delete the frames we made
done
