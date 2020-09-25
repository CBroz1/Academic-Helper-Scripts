# @Author: christopherbrozdowski
# @Date:   2017-08-30 14:39:06
# @Last Modified by:   cb
# @Last Modified time: 2020-09-25 15:40:03

#Purpose: overlay multiple videos

ffmpeg -y \
		# list all input videos. 0-indexed list for alter
    -i base.mp4 -i sm1.mp4 -i sm2.mp4 \
    -i sma.mp4 -i smb.mp4 -i smc.mp4 \
    # null base for overlaying [name for it]
    # [foundation][0-index newvid] \
    # shortest 1y 0n, x/y coord of topleft corner [newlabel]
    -filter_complex "
    nullsrc=size=1920x1440 [base];
    [base][0:v] overlay=shortest=0 [tmp1];
    [tmp1][1:v] overlay=shortest=0:x=96:y=112 [tmp2];
    [tmp2][2:v] overlay=shortest=0:x=1152:y=112 [tmp3];
    [tmp3][3:v] overlay=shortest=0:x=52:y=960 [tmp4];
    [tmp4][4:v] overlay=shortest=0:x=701:y=960 [tmp5];
    [tmp5][5:v] overlay=shortest=1:x=1376:y=960 [out]
    " \
    -map "[out]" \
    -c:v libx264 output.mp4

## set shortest 0 until last. if all 0, infinite length
