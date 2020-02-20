# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:12:33

#Purpose: generate duration information of mp4 files in current dir
#Caution: for loop targets mp4 files

for f in *mp4
do
	#echo $f
	ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $f
done

#open pic_test$1.pict