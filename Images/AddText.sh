# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:42:44

#Purpose: Add the same text to many png files
# could easily be changed to vary text


for f in *png
do
	convert $f  -fill white  -undercolor '#00000080' -pointsize 90 -gravity South \
          -annotate +0+100 'Press SPACE to continue' $f
done

#open pic_test$1.pict