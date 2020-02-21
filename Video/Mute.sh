# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-02-21 15:09:03

mkdir -p ./Muted/

for f in *.mp4
do
	ffmpeg -i $f -c copy -an ./Muted/$f
done

### UNUSED ### /2 = 360x240 
	#j=$(printf "%03d" $i)
	#LAST_num=${LAST_fi:${#f}+5:3}
	#LAST_num=$( printf "%.0f" $LAST_num )
	#LAST_num_sec=$((LAST_num+25))
	#echo $LAST_num_sec
	#for ((i=$LAST_num;i<=($LAST_num+25);i++)); do
	#for i in $(seq $LAST_num $LAST_num_sec); do