#!/bin/tcsh -f
# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 19:39:01

set InFile = $argv[1]
set InFileH = `echo $InFile | tr _ -` #Change _ to -, cause xmats have _ but 1ds hav -

set noise = $argv[2]
set model = $argv[3]
set SepNoi = '_Noi'
set SepMod = '_Mod'
set OutFile = ${InFile}${SepNoi}${noise}${SepMod}${model}
set nfirst = 0
set nlast = 719
set polort = 1
set seed = 123

foreach num ( 0 1 2 3 4 5 6 7 8 9)
	1dcat $InFile.xmat.1D"[$num]" > cat_${num}.1D
end

echo "100.0" > Base.1D
echo "0.0" >> Base.1D

# set hrf  effect size (can change them individually later)  
foreach numh (1 2 3 4 5 6 7 8 9 10)
	echo "1.0" > h${numh}.1D
end

#1dcat 
3dConvolve 					\
	-input1D 				\
	-nfirst $nfirst 		\
	-nlast $nlast			\
	-polort $polort			\
	-base_file Base.1D 		\
	-sigma $noise 			\
	-seed $seed				\
	-num_stimts 4	 		\
	-stim_file 1  cat_6.1D  \
	-stim_file 2  cat_7.1D  \
	-stim_file 3  cat_8.1D  \
	-stim_file 4  cat_9.1D  \
	-iresp 1 h1.1D 			\
	-iresp 2 h2.1D 			\
	-iresp 3 h3.1D 			\
	-iresp 4 h4.1D 			\
	-output ${OutFile}_Conv_TS  

1dplot ${OutFile}_Conv_TS.1D

echo $OutFile > 3dDecon_Output_${InFile}

3dDeconvolve                                                  \
	-input1D ${OutFile}_Conv_TS.1D\'                          \
	-polort $polort		                                          \
	-TR_1D 2        	                                      \
	-num_stimts 4                                             \
	-stim_times 1 stimes_8sResp_${InFileH}_Cond1.1D $model     \
	-stim_label 1 Cond1                                        \
	-stim_times 2 stimes_8sResp_${InFileH}_Cond2.1D $model     \
	-stim_label 2 Cond2                                        \
	-stim_times 3 stimes_8sResp_${InFileH}_Ctrl.1D $model     \
	-stim_label 3 Ctrl                                        \
	-stim_times 4 stimes_8sResp_${InFileH}_Resp.1D $model     \
	-stim_label 4 Resp                                        \
	-iresp 1 IR_${OutFile}_Cond1								  \
	-iresp 2 IR_${OutFile}_Cond2								  \
	-iresp 3 IR_${OutFile}_Ctrl								  \
	-iresp 4 IR_${OutFile}_Resp								  \
	-tout	                                                  \
	-x1D ${OutFile}.xmat.1D 								  \
	-fitts FittModel_8sResp_${OutFile}				          \
	-gltsym 'SYM: +Cond1 +Cond2 +Ctrl +Resp' -glt_label 1 FullF \
	-gltsym 'SYM: +Cond1 +Cond2 -Ctrl' -glt_label 2 ExpVCtrl    \
	-gltsym 'SYM: +Cond1 -Ctrl' -glt_label 3 Cond1VCtrl         \
	-gltsym 'SYM: +Cond2 -Ctrl' -glt_label 4 Cond2VCtrl         \
	-gltsym 'SYM: +Cond1 -Cond2' -glt_label 5 Cond1VCond2         \
	>> 3dDecon_Output_${InFile}

    
# consider plotting the SUM below non-polort regressors
# command: 1dplot -xlabel Time X.xmat.1D'[5]'

1dplot -one  						\
	-xlabel Time 					\
	-ylabel "HRF curve" 			\
	-ynames  Cond1 Cond2 Ctrl Resp - 	\
	IR_${OutFile}_Cond1.1D   		\
	IR_${OutFile}_Cond2.1D   		\
	IR_${OutFile}_Ctrl.1D   		\
	IR_${OutFile}_Resp.1D   
