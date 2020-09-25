#!/usr/bin/env python
# Goal: Change R(Cond) to 4s Cond, 2s NULL, 2s R(Cond)
#cmd: cd [path]/Optseq_CB/TestEnv/1
#cmd: python ../../_Scripts/ConvParRPar.py

TR = 1                                    #fMRI TR in Sec, 1D row duration
#                                         #if using stim_times, keep at 1
Conds = ['Cond1', 'Cond2', 'Ctrl', 'NULL']
#                                         #Experimental Conditions and NULL
Cond = Conds[:-1]                         #Conditions only
LABELS = " ".join(Cond)                   #stim_time files labeled by condition
PREFIX = "stimes"                         #make_stim_times files prefix
NRUNS = 2 #changed from 1                 #number of runs, default 1
NT = 0                                    #change to force number of TRs per run
#   #if <7min run, defaults to full 1D as run, otherwise divides to sub 7min runs
count_1D = 0

import glob, os                           #importing glob for listing files
from os import rename, listdir            #os, renaming, remove make_stim count

ParFiles = glob.glob("O*.par")          #List all .par files in current dir
Par_NoExt = [x.strip('.par') for x in ParFiles] #drop .par extension

def ConvertParRPar(ParName):
    count_par = 1                 #Count lines in ParFile
    global count_1D               #Needed to modify global copy
    count_Resp = 0                  #Count lines in 1D
    Par_NoPre = ParName.split('_',1)[1]
    for line in open("%s.par" % ParName):
        line = line.strip('\n')        #Remove any \n and \t from line
        parts = line.split("   ")  #Split on 3 spaces
        b = "   "
        Dur = parts[2]             #Duration is Column 3
        ConL_Space = parts[6]      #Condition Label Column 7, with leading space
        Dur = float(Dur)           #Declare Dur as float
        CondLabel = ConL_Space[1:] #Remove leading space
        RConds = ["R" + Cond for Cond in Conds]
        f = open("R%s.par" % (ParName), 'a')
        if ConL_Space in RConds:   
            f.write("%s   %s    4.000   1.0000          %s\n" % (parts[0], parts[1], ConL_Space[1:])) #Stim
            f.write("%s   %s    2.000   1.0000          NULL\n" % (parts[0], parts[1]))
            f.write("%s   %s    2.000   1.0000          Resp\n" % (parts[0], parts[1]))
            count_Resp += 1
        else:
            f.write("%s\n" % line)    #Write 0 and newline in Others.1D
        f.close()                #Close Condition file
        count_par += 1
    rows_1D = count_1D / len(Conds)
    print "%s: %d lines converted, %d Resp items\n" % (ParName, count_par, count_Resp)
    #                          #number of lines converted and printed to console

def main():
    print "appending existing R*.par files"
    for elem in Par_NoExt:           #For every par file in dir
        ConvertParRPar("%s" % elem)       #remove RStim, replace with stim null resp
def main_Only1(LonePar):            #main() for just one par file
    Clear1Ds("%s" % LonePar)
    ConvertPar1D("%s" % LonePar)
    StimTimes("%s" % LonePar)
    CleanSTimes
#main_Only1("Temp.par")          #Convert one .par, Replace 'Temp' with filename
main()                           #Convert all .par in current directory
