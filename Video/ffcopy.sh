# arg1 seconds
# arg2 file

while getopts ":h" option; do
   case $option in
      h|help) # display Help
         echo "Arg1 - first X seconds of clip"
         echo "Arg2 - clip filepath"
         echo "Does - First X seconds saved as filepath-copy{same ext}"
         exit;;
   esac
done

filename_full="$2"
filename=${filename_full%%.*}
ext=${filename_full##*.}

ffmpeg -n -hide_banner -loglevel error -ss 0 -t $1 -i $filename_full \
-vcodec copy -acodec copy ${filename}-copy.${ext}
