# @Author: jinwang
# @Date:   
# @Last Modified by:   cb
# @Last Modified time: 2020-09-25 16:05:09
#! /bin/bash

###PURPOSE
## Generate binary mask of top X voxels for each subject
## from SPM t-maps, using afni functions, in an fmri analysis 

###NOTES 
## Jin Wang and Macarena Suarez developed original code (maskdump/3dcalc)
## Chris Brozdowski front-loaded variables, and added loop for contrasts 

project=redacted/project/path		#project folder with subj subjfolder and rois sujbfolder
subjfolder=${project}/preproc 	#individ subj folders are here
rois=${project}/rois 						#rois folder
analysisfolder=analysis 				#within subj, analysis folder name, with spmT contrast files
contrastnum=(03 04)							# contrast numbers, from 1st level analysis
contrastname=("XY" "ZZ") 				# names of these contrasts
roilist=("ABC" "DEF")						# list of rois for which you have mask files
#CAUTION: $roifile defines prefix and suffix on actual roi file. must change
topvox=(100)										# number of top voxels. 100 is common

#CAUTION: "p1_" naming convention may need changing for you

## subject numbers
subjnums=(01 08 09 10 11 13 14 16 17 19 \
				 	21 24 25 29 31 32 33 35 36 37 \
					41 42 43 44 47 48 49 51 56 57 \
					58 60 61 68 71 75 76 77 80 81 83 84) 
## subject prefix, here 'sub-'
subjlist=("${subjnums[@]/#/sub-}")

for num in ${topvox[@]}
do
	for roi in ${roilist[@]} 								# these are mask names
	do 
		roifile="mask_${roi}_81.hdr"   				# actual mask file - change this   
		for ((i=0;i<${#contrastnum[@]};++i))  # loop through contrasts numbers
		do
			roicon="${roi}_${contrastname[i]}"	# string concatenate
			mkdir -p ${rois}/${roicon}_p1_k${num} # mkdir for roi, p1_k is name convention
			cd ${rois}/${roicon}_p1_k${num}			
			for subj in ${subjlist[@]}					# for subject in list
			do
				mkdir -p ${subj}									# make subject directory
				cd ${rois}/p1_k${num}_${roicon}/${subj}/

				echo "${roicon} ${subj}"

				# find the coordinates and the t-values within a mask. 
				3dmaskdump \
				-mask ${rois}/${roifile} \
				${subjfolder}/${subj}/${analysisfolder}/spmT_00${contrastnum[i]}.nii > \
				${roicon}_output.txt

				# sort the output.txt to select the top $num numbers. JW
				sort -rk4 -n ${roicon}_output.txt | head -${num} > ${roicon}_top${num}.txt
				awk '$4+=1000' ${roicon}_top${num}.txt > ${roicon}_top${num}_adjust.txt

				# put these top 100 back to brain #master to make same dimension as orig results
				3dUndump \
				-prefix ${roicon}_p1_k${num}_adjust.nii \
				-master ${subjfolder}/${subj}/${analysisfolder}/spmT_00${contrastnum[i]}.nii \
				-ijk ${roicon}_top${num}_adjust.txt
				 
				# make a mask of these 100 voxels (make them equal to 1)
				3dcalc -a ${roicon}_p1_k${num}_adjust.nii -expr 'ispositive(a)' \
				 -prefix ${roicon}_p1_k${num}_mask_adjust.nii
			done # End subj loop		
		done # End contrast Loop
	done #End ROI loop
done #end num loop