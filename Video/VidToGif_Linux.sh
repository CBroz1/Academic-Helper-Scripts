# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:39:30

# Caution: VidToGif_Mac has more commenting for ease of use

mkdir -p zFrames
touch _Info.txt

for f in *.m*
do
	echo ${f%.*}
	ffmpeg -loglevel error -i $f -qscale:v 2 -vf fps=25 zFrames/${f%.*}-%03d.jpg
	LAST_fi=`exec ls zFrames/*jpg | sed 's/\([0-9][0-9][0-9]\+\).*/\1/g' | sort -n | tail -1`
	LAST_num=$( printf "%.0f" ${LAST_fi:${#f}+6:4} )
	echo $LAST_num
	echo "${f%.*}, $LAST_num" >> _Info.txt
	for i in `seq $((LAST_num+1)) $((LAST_num+13))`; do
		cp $LAST_fi.jpg zFrames/${f%.*}-$(printf "%03d" $i).jpg
	done
	convert -delay 4 -loop 0 zFrames/${f%.*}*.jpg -resize 50% +repage -layers optimize ${f%.*}.gif
	rm zFrames/${f%.*}*.jpg
done