
# Stimuli Manipulation

Over my career, I've put time into learning tools that allow me to automatically generate videos, images, or text files for experimental stimuli or even data management. I post them here to preserve copies for future use, as well as share them with peers. The specifics of each script will have to be changed to fit future projects, but each can serve as a framework for accomplishing similar tasks.

## Patterns

**sh renaming**: I've found it very useful to use the following to juggle files with string substitution

```console
for file in $(ls -f /path/); do
	echo ${file%%.*} # filename before first `.`
	echo ${file%.*}  # filename before last `.`
	echo ${file#*.}  # extension after first `.`
	echo ${file##*.} # extension after last `.`
	echo ${file/find/replace} # replace substring

done
```

**paired arrays**: Using two arrays, you can pair files and labels.

```console
array1=("A.txt" "B.txt" "C.txt")
array2=("One" "Two" "Three")

for ((i=0;i<${#array1[@]};++i)); do
    printf "%s matches %s\n" "${array1[i]}" "${array2[i]}"
done
```

**conditional from args**: While a more advanced approach would use argument flags, I've found it accessible to run portions of scripts based on the value of a positional argument.

```console
if [[ $1 -eq 2 ]]; then # if positional 1 equals 2
	echo "Ran 2"		
fi
```

**dating output**: `mydate_variable=$(date +"%m%d%y")`

## Video

Most of my video editing relies on [`ffmpeg`](https://github.com/FFmpeg/FFmpeg#ffmpeg-readme), which is easiest to install via [`homebrew`](https://brew.sh/). Some text features of `ffmpeg` may require specific installation parameters.

- *Watermark:* Don't you wish your stimuli could show a code in the corner for experimenter use? Like condition and stimulus specifics? This script, by default, uses a substring of the filename as text in a watermark in the corner.
- *Watermark_Mult:* Cycles through multiple different labels for watermarking videos. Good example of embedded looping.
- *Hold_Last_Frame:* Does your (fMRI or Working Memory) experiment require that all videos in a directory are exactly the same duration? Do you wish you could use that last frame as your ISI? This script extends the last frame of a video clip to a target duration. 
- *Hold_Last_Frame_Loop:* Puts the above information in a for loop. 
- *LastFrame:* Generates png of last frame of a video clip.
- *ffcopy:* Copy first X seconds of given video Y, append `-copy` to filename
- *GetDur:* Generate duration of input video clip.
- *Crop:* Do you have a lot of videos that are too zoomed out? This script first generates a mean image for many videos (using first or all frames), to make sure your various videos are lined up, and then crops based on user measurement of xy coordinates.
- *Mute:* Generates a muted copy of all mp4 files in a directory, moved to a ./Muted subfolder.
- *OverlayVids:* Takes multiple source videos and outputs an overlay. Must be edited with xy values.
- *GreenScreen:* Replace green background with neutral grey.
- *Green_Concat:* Project specific workflow for chroma-keying, watermarking, picture to video, and concatenating video for experimental presentation. General tip for concatenation: use mkv.
- *VidToGif_Mac:* Batch turn video clips into gif files, at 50% resolution. Some components of this process should change if running Linux, but Mac version of this script is better commented.

## Images

Here, a lot of editing relies on [ImageMagick](https://imagemagick.org/index.php), using the `convert` command. 

- *AddText:* Add text to bottom of png files.
- *ColorNegate:* Negate image colors
- *ConvertToPict:* Convert pngs to pict files, specifically for Psyscope.
- *GenImgsOfText:* For single word presentation study using images, because native text presentation in software isn't ideal if you're alternating between orthography and control images, of false fonts, for example.

## Text

I'm a big advocate of [Sublime Text](https://www.sublimetext.com/) as a text editor with powerful integrated tools. I even use Sublime for note taking purposes, and have made a [tutorial video](https://www.youtube.com/watch?v=v_FENArHqFU) to go into more detail. For anything that can't be handled in a couple lines of Unix, I would turn to python or R, depending on collaborator preference..

- *nback_rhyme_task:* takes a list of words from a database with orthographic 'body' and phonological 'rime' information, and generates possible stimuli lists for a rhyme judgement nback task. Some psycholingusitic paradigms push the bounds of what's possible with a given word list. This script takes the guesswork/trial-and-error our of the development process.
- *Randomizer_For_Eprime:* Eprime offers limited randomization options, so researchers often turn to limited pseudorandomized preset lists to obey certain constraints. What if you could run one exe that would randomize according to limitations you set, and then just open the software automatically?
- *TextToSpeech:* Too much reading? Listen instead! Relies on OSX `say` command, which, in my experience, is a lot higher quality than other software.
- *LineBreaks:* Line breaks are saved differently depending on OS and can interfere with UNIX execution. I use this as a sanity check on scripts.
- *zeroPading:* Adds padded zeros to numbered jpg files
- *FZ:* Old personal project taking user survey input and cross referencing responses against all other users. Learned a lot of lessons on debugging, passing parameters to run subsets of a script, and complex data structures like tuples. 

## fMRI

Some of these files are specific to an fMRI project I was involved in. They hard code a lot of information, including stimulus timing, stimulus names, etc. They highlight the extended process of simulating that dataset, but also how to generate subject-specific video stimuli based on experiment timing files. I was not the lead on this project, and these scripts *do not represent the final outcome*, but only the first draft of such functions used in my own learning process.

- *OptSeq:* Parameters passed to the afni OptSeq command.
- *ConvParRPar:* Specific our fMRI paradigm, converting par files to rpar files for simulating event related paradigm data.
- *Loop_ConDecon:* Loops through the similarly named `Con_DeCon.sh` file with various levels of noise and hemodynamic response function values.
- *ConvParVid:* Once we had simulated the data, automatically generates video files for each subject based on OptSeq par files. 
- *Top_Voxel_Indiv:* TopVoxel analysis tool. Credit to Jin Wang & Macarena Suarez.
- *tal2label:* This R script generates anatomical labels for Talairach coordinates, calling on SPM's tal2mni function and using the [label4MRI](https://github.com/yunshiuan/label4MRI) R package.

## File management

### Archiving

The following helps archive file systems:

```console
rsync -hraP --ignore-existing /Source /Destination
```

with these parameters:
- h human readable
- r recursive
- a archive
- P show progress
- --ignore-existing

### Finding duplicates

`fdupes` can help list duplicates, but I want to allow for duplicates in some places. The following command ignores zero-length files and removes patterns, like directories, pulled from a text file.

```console
fdupes -nr . | grep -v -f permitted.txt > duplicates.txt
```

The output leave singleton lines (breaks on either side) representing the duplicates of files in permitted places.