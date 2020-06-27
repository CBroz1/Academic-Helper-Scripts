# @Author: CB
# @Date:   2017-05-23 18:21:56
# @Last Modified by:   local-admin
# @Last Modified time: 2020-06-27 09:38:43

## takes argument at command line to execute subsets of code
    # most depends on installation of ImageMagick - recommended via homebrew
    # 1 generates bmp images on a standard 455 by 125 blank canvas
    #   writes on the image a set of words defined by _list.txt
    # 2 converts preexisting font png files to bmp files
    # 3 looks at a list of ExpName\tFileName, copy all images to relevant task subfolder

# generating pictures of single words
while IFS='' read -r line || [[ -n "$line" ]]; do       # read lines from .txt below
    if [[ $1 -eq 1 ]]                                   # if cmdline arg == 1
    then
        convert -size 455x125 xc:white blank.png        # make a white image
        echo "Text: $line"                              # echo text and output file name
        out="T_${line%}.bmp"
        echo "Out: $out"
        convert blank.png -font Arial -pointsize 96 \           # use .txt line to write on blank img
        -draw "gravity east fill black text 10,3 '$line'" $out
        mkdir -p Read_All/                                     # make dir for new images
        mv T*bmp Read_All/                                     # move new images there
    fi
done < "./_list.txt"

# converts a set of files to bmp format, which is faster for eprime
if [[ $1 -eq 2 ]]
then
    for f in _F*png
    do
        echo "${f%.*}.bmp"
        convert $f ${f%.*}.bmp
    done
fi

# Sort images based on TxtByExp list, which can be pulled from a spreadsheet
# TxtByExp should be two columns sep by tab: ExpName and ExpFile with extension 
if [[ $1 -eq 3 ]]
then
    while IFS='' read -r line || [[ -n "$line" ]]; do
        # mkdir -p ${line##*$'\t'}               # make dir if not exist
        cp -n Read_All/${line##*$'\t'} ${line%%$'\t'*}/ # copy no overwrite
    done < "./TxtByExp.txt"
fi



