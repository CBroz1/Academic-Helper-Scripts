# @Author: CB
# @Date:   2017-05-23 18:21:56
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 17:58:53

array1=("SL01_N.mp4" "SL01_B.mp4" "SL01_H.mp4" "GL01_N.mp4" "GL01_B.mp4" "GL01_H.mp4")
array2=("Example Normal Pseudosign" "Example Blurred Pseudosign" "Example Hold Pseudosign" "Example Normal Grooming Gesture" "Example Blurred Grooming Gesture" "Example Hold Grooming Gesture")

for ((i=0;i<${#array1[@]};++i)); do
    # printf "%s is in %s\n" "${array1[i]}" "${array2[i]}"
    echo ${array1[i]}
	ffmpeg -loglevel info  -y -i ${array1[i]} -vf scale=1280:720 \
	drawtext='fontfile=/Library/Fonts/Times\ New\ Roman\ Bold.ttf: \
	text='${array2[i]}': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
	boxborderw=5: x=x=(main_w/2-text_w/2): y=main_h-(text_h*2)' \
	-codec:a copy ./Edits/${array1[i]}.mp4
done
