# @Author: CB
# @Date:   2017-05-23 18:21:56
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 11:59:51

# Purpose: add text to videos
# Use - default dry run, pass 1 as arg for actual run
# on ffmpeg install, check drawtext installation

# drawtext is source of font
# fontcolor, size and boxcolor change appearance
# x and y are text position


files="./*.m*" # Path of videos we'll be editing
for InFi in $file
do
	Label=${InFi:8:7} # Text we'll be addiing to the video
										# here, substring of file name
	InFi_NoSuf=${InFi:0:15} # input file, no suffix
	echo $Label
	echo $InFi_NoSuf
	mkdir -p zWithLabel/    # make dir for output files
	if [ $1 -eq 1 ]
		then
		ffmpeg -loglevel info  -y -i $InFi -vf \
		drawtext='fontfile=/Library/Fonts/Times\ New\ Roman\ Bold.ttf: \
		text='$Label': fontcolor=white: fontsize=18: box=1: boxcolor=black@0.5: \
		boxborderw=5: x=(text_h): y=main_h-(text_h*2)' \
		-codec:a copy ./zWithLabel/$InFi_NoSuf.mp4
		#linux: fontfile=/usr/share/fonts/truetype/lato/Lato-Regular.ttf
		#mac: fontfile=/Library/Fonts/Times\ New\ Roman\ Bold.ttf
		#zWithLabel/
		#mv $InFi zNoLabel/
	fi
	
	#mv zWithLabel/$InFi ./

	Finish='DONE: '; Finish+=$InFi
	echo $Finish 
done