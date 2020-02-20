# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:44:10

#Purpose: invert images
#personally used to change from light to dark ppt theme

for f in $1*.png # pass arg for image prefixes
do
	echo ${f%.*}
	convert $f -channel RGB -negate ${f%.*}_BW.png
done
