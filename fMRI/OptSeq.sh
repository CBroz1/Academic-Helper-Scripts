#!/bin/tcsh
# optseq2 example, CB modified 26/08/16, Version 5
# Includes 8s response items for each condition

set out = OptSeq_8sResp

set ntp = 356           # Num time points. Sum(Stim*Dur)+prescan #sum(tEv*nReps)(nEv+1)/nEv <= Ntp*TR+tprescan    
set tr = 2
set nEv = 6             # number of events
set tprescan = 8        # dummy scans
set psdmin = 0          # PostStim Delay minimum
set psdmax = 12         # PostStim Delay max
set dpsd = 1            # PostStim sampling interval
set tEv = 4             # Cond duration in seconds, integers only 
set nReps = 19          # Cond reps
set tEv_Resp = 8        # Resp dur
set nReps_Resp = 5      # Resp reps
set tnullmin = 2        # minimum duration of null event (e.g. ISI)
set tnullmax = default  # not used
set polyfit = 2
set nsearch = 100000    # search through 100k iterations
set tsearch = 1         # 1 hour searching  # not used
set nkeep = 10          # keep X .par files
set focb = nCB1Opt      # Dont change
set seed = 123456
set evc = "1 -1 0"      # Optional, unused
OptSeq2 \
                --ntp ${ntp} \
                --tr  ${tr} \
                --tprescan ${tprescan} \
                \
                --psdwin ${psdmin} ${psdmax} ${dpsd} \
                --ev Cond1 {$tEv} $nReps \
                --ev Cond2 {$tEv} $nReps \
                --ev Ctrl {$tEv} $nReps \
                --ev RCond1 {$tEv_Resp} $nReps_Resp \
                --ev RCond2 {$tEv_Resp} $nReps_Resp \
                --ev RCtrl {$tEv_Resp} $nReps_Resp \
                --tnullmin ${tnullmin} \
                \
                --nsearch ${nsearch} \
                --nkeep ${nkeep} \
                --polyfit ${polyfit} \
                --focb ${focb} \
                #--evc ${evc} \
                --seed ${seed} \
                \
                --o ${out}_sched \
                --sum ${out}_summary \
                --log ${out}_log
