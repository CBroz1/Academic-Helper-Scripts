# -*- coding:  utf-8 -*-
# @Last Modified by:   Chris
# @Last Modified time: 2016-11-24 13:49:33
#!/usr/bin/env python

# Goal: Take ALL current directory .par files (OptSeq2)
#       Convert to binary .1D files then stimes
#       This version only has one stimes row to facilitate 3dDeconv
# NOTES TO SELF: doesn't impliment response item conversion from ConvParRPar
#                ADDED resp to Conds for ConvParRPar file setup
#               Modified NRuns to 1, and NT to 760 so can run 3dDecon easier

TR = 1  # fMRI TR in Sec, 1D row duration
#                                         #if using stim_times, keep at 1
Conds = ["Proj", "Topo", "Ctrl", "Resp"]
#                                         #Experimental Conditions and NULL
Cond = Conds[:-1]  # Conditions only
LABELS = " ".join(Conds)  # stim_time files labeled by condition
PREFIX = "stimes"  # make_stim_times files prefix
NRUNS = 1  # changed from 3                 #number of runs, default 1
NT = 720  # Changed from 0                  #change to force number of TRs per run
#   #if <7min run, defaults to full 1D as run, otherwise divides to sub 7min runs
count_1D = 0

import glob, os  # importing glob for listing files
from os import rename, listdir  # os, renaming, remove make_stim count

ParFiles = glob.glob("*.par")  # List all .par files in current dir
Par_NoExt = [x.strip(".par") for x in ParFiles]  # drop .par extension


def ConvertParRPar(ParName):  # NOT IMPL HERE, Sep file
    count_par = 1  # Count lines in ParFile
    global count_1D  # Needed to modify global copy
    count_Resp = 0  # Count lines in 1D
    Par_NoPre = ParName.split("_", 1)[1]
    for line in open("%s.par" % ParName):
        line = line.strip("\n")  # Remove any \n and \t from line
        parts = line.split("   ")  # Split on 3 spaces
        b = "   "
        Dur = parts[2]  # Duration is Column 3
        ConL_Space = parts[6]  # Condition Label Column 7, with leading space
        Dur = float(Dur)  # Declare Dur as float
        CondLabel = ConL_Space[1:]  # Remove leading space
        RConds = ["R" + Cond for Cond in Conds]
        f = open("R%s.par" % (ParName), "a")
        if ConL_Space in RConds:
            f.write(
                "%s   %s    4.000   1.0000          %s\n"
                % (parts[0], parts[1], ConL_Space[1:])
            )  # Stim
            f.write("%s   %s    2.000   1.0000          NULL\n" % (parts[0], parts[1]))
            f.write(
                "%s   %s    2.000   1.0000          R%s\n"
                % (parts[0], parts[1], ConL_Space[1:])
            )
            count_Resp += 1
        else:
            f.write("%s\n" % line)  # Write 0 and newline in Others.1D
        f.close()  # Close Condition file
        count_par += 1
    rows_1D = count_1D / len(Conds)
    print(
        "%s: %d lines converted, %d Resp items\n" % (Par_NoExt, count_par, count_Resp)
    )
    #                          #number of lines converted and printed to console


def Clear1Ds(ParName):  # Clear existing 1D files for the .par
    Par_NoPre = ParName.split("_", 1)[1]
    for elem in Conds:
        with open("%s_%s.1d" % (Par_NoPre, elem), "w"):
            pass


def ConvertPar1D(ParName):
    count_par = 1  # Count lines in ParFile
    global count_1D  # Needed to modify global copy
    count_1D = 0  # Count lines in 1D
    Par_NoPre = ParName.split("_", 1)[1]
    for line in open("%s.par" % ParName):
        line = line.strip()  # Remove any \n and \t from line
        parts = line.split("   ")  # Split on 3 spaces
        Dur = parts[2]  # Duration is Column 3
        ConL_Space = parts[6]  # Condition Label Column 7, with leading space
        Dur = float(Dur)  # Declare Dur as float
        CondLabel = ConL_Space[1:]  # Remove leading space
        for elem in Conds:  # Cycle through Conditions
            TRs = Dur / TR  # Rows as fmri TR, not sec
            f = open("%s_%s.1d" % (Par_NoPre, elem), "a")  # Create/append 1Ds
            while TRs > 0:  # Until TR <= 0, meaning round up
                if elem == CondLabel or elem == ConL_Space:
                    f.write("1\n")  # Write 1 and newline in Condition.1D
                    count_1D += 1
                else:
                    f.write("0\n")  # Write 0 and newline in Others.1D
                    count_1D += 1
                TRs -= 1  # Decriment TR count
        f.close()  # Close Condition file
        count_par += 1
    rows_1D = count_1D / len(Conds)
    print("%s: %d lines converted, printed %d to 1d" % (ParName, count_par, rows_1D))
    #                          #number of lines converted and printed to console


def StimTimes(ParName):
    global NT
    global NRUNS
    rows_1D = count_1D / len(Conds)
    # if NT == 0:                #if user doesn't set NT, cut runs to sub 7m
    #    while (1 * rows_1D / NRUNS >= 420):
    #        NRUNS += 1
    #    NT1 = (rows_1D / NRUNS)
    # else:
    NRUNS = 1  # added
    NT1 = NT
    Par_NoPre = ParName.split("_", 1)[1]  # Delete existing stimes files for Par
    for filename in glob.glob("%s_%s*" % (PREFIX, Par_NoPre)):
        os.remove(filename)
    OneDFiles = []  # declare null list
    for C in Conds:  # make list of .1d files for each par
        OneDFiles.append("%s_%s.1d" % (Par_NoPre, C))
    FILES = " ".join(OneDFiles)  # join 1d list to string
    #                                #set commandline input as string
    cmd = """make_stim_times.py \\
    -files %s \\
    -prefix %s_%s_ \\
    -nruns %s \\
    -nt %s \\
    -tr %s \\
    -labels %s""" % (
        FILES,
        PREFIX,
        Par_NoPre,
        NRUNS,
        NT1,
        TR,
        LABELS,
    )
    os.system(cmd)  # run command


def CleanSTimes():
    fnames = listdir(".")  # remove added number from stimes files
    for fname in fnames:
        if fname.startswith("stimes"):  # for all stimes files
            parts = fname.split(".")  # split on periods
            del parts[1]  # delete second item
            parts[2] = "." + parts[2]  # add period before 1d
            rename(fname, "".join(parts))  # rename as joined parts


def RenamePar():
    print("\nde-comment to rename files.\n")
    fnames = listdir(".")
    for fname in fnames:
        if fname.endswith(".par"):
            parts = fname.split("_")  # split on underscore
            parts[0] = parts[0] + "_"
            # rename(fname, ''.join(parts)) #rename as joined parts


def main():
    for elem in Par_NoExt:  # For every par file in dir
        #        Clear1Ds("%s" % elem)         #Clear existing 1D specific to par
        #        ConvertPar1D("%s" % elem)     #Convert par to 1D
        #        StimTimes("%s" % elem)        #run make_stim_times.py
        ConvertParRPar("%s" % elem)
    CleanSTimes()


def main_Only1(LonePar):  # main() for just one par file
    Clear1Ds("%s" % LonePar)
    ConvertPar1D("%s" % LonePar)
    StimTimes("%s" % LonePar)
    CleanSTimes


# main_Only1("Temp.par")          #Convert one .par, Replace 'Temp' with filename
main()  # Convert all .par in current directory
