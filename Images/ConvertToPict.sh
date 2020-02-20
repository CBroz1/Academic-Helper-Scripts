# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   Chris
# @Last Modified time: 2017-09-24 14:34:07


for f in *png
do
	convert $f ${f%.*}.pict
done

