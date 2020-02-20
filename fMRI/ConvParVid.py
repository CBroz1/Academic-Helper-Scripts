#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Chris
# @Date:   2016-11-15 14:49:37
# @Last Modified by:   Chris
# @Last Modified time: 2017-01-12 02:10:52

## Notes
    # Makes single ffmpeg cat file for each par
    # Runs ffmpeg cat
    # Makes multi cat file, leaving resp movies sep
        # for all sched listed in Split Sched
    # Runs ffmpeg cat on sched subsets, copies resp movies over
## DO
    # Make NULL.mov, make End.mov
    # Run as is with print to remake _PsyRun files

import glob, os, time                            #importing glob for listing files
from random import randint, shuffle

ParFiles = glob.glob("O*.par")                   
Par_NoExt = [x.strip('.par') for x in ParFiles]  #drop .par extension
InputFiles = glob.glob("*txt")
InFi_NoExt = [x.strip(".txt").strip("IN_") for x in InputFiles]
SplitSched = ["001"]                              #MOD here for more split

Conds = ['Proj', 'Topo', 'Ctrl', 'NULL']
RConds = ["R" + Cond for Cond in Conds]
VProj = ['01', '02', '03', '05', '06', '08', '09', '10', '11', '13', '15', '16', '18', '19', '20', '21', '22', '23', '24'] 
VTopo = ['26', '27', '28', '30', '31', '33', '34', '35', '36', '37', '38', '40', '42', '43', '44', '45', '46', '47', '48'] 
VCtrl = ['49', '50', '51', '53', '54', '55', '57', '58', '59', '61', '62', '64', '66', '67', '68', '69', '70', '71', '72']
VRProj = ['04_Y', '07_N', '12_Y', '14_Y', '17_N']
VRTopo = ['25_N', '29_N', '32_N', '39_Y', '41_Y']
VRCtrl = ['52_Y', '56_N', '60_N', '63_Y', '65_Y']

def MakeCatList(ParName):  
    Sched = ParName[-3:]
    count_par = 0                                 #Lines in ParFile
    for i,j in zip(Conds, RConds):                #count_Cond set to 0
        exec("count_%s = %d" % (i,0))
        exec("count_%s = %d" % (j,0))
    for i in [VProj, VTopo, VCtrl, VRProj, VRTopo, VRCtrl]:
        shuffle(i)                                #Randomize lists
    EngF = open("IN_Eng_%s_ALL.txt" % (Sched), 'w+')  # W+ truncates to 0, permits read
    AslF = open("IN_ASL_%s_ALL.txt" % (Sched), 'w+')
    ResF = open("IN_Resp_%s_ALL.txt" % (Sched), 'w+')
    ResF.write("Stim\tCond\tResp\n")
    for line in open("%s.par" % ParName):
        parts = line.strip('\n').split("   ")     #Remove \n, Split on 3 spaces
        Dur = float(parts[2])                     #Duration is Column 3
        CondLabel = parts[6].strip( ' ' )
        if float(parts[0]) < 356 and float(parts[0]) + Dur > 365:
        	print "-------BRIGES GAP-------"
        	with open("_ERROR", "a") as err:
			    err.write("%s Bridges Run Gap\n" % (Par_NoExt))
        if CondLabel == "RProj":
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VRProj[count_RProj][:2]))
            EngF.write("file 'NULL.mov'\nfile 'NULL.mov'\n")
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VRProj[count_RProj]))
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VRProj[count_RProj][:2]))
            AslF.write("file 'NULL.mov'\nfile 'NULL.mov'\n")
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VRProj[count_RProj]))
            ResF.write("Stim_TopoProj_%s.mov\tProj\t%s\n" % (VRProj[count_RProj], VRProj[count_RProj][-4:-3]))
            count_RProj += 1
        if CondLabel == "RTopo":
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VRTopo[count_RTopo][:2]))
            EngF.write("file 'NULL.mov'\nfile 'NULL.mov'\n")
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VRTopo[count_RTopo]))
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VRTopo[count_RTopo][:2]))
            AslF.write("file 'NULL.mov'\nfile 'NULL.mov'\n")
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VRTopo[count_RTopo]))
            count_RTopo += 1
        if CondLabel == "RCtrl":
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VRCtrl[count_RCtrl][:2]))
            EngF.write("file 'NULL.mov'\nfile 'NULL.mov'\n")
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VRCtrl[count_RCtrl]))
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VRCtrl[count_RCtrl][:2]))
            AslF.write("file 'NULL.mov'\nfile 'NULL.mov'\n")
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VRCtrl[count_RCtrl]))
            count_RCtrl += 1
        if CondLabel == "Proj":
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VProj[count_Proj]))
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VProj[count_Proj]))
            count_Proj += 1
        if CondLabel == "Topo":
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VTopo[count_Topo]))
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VTopo[count_Topo]))
            count_Topo += 1
        if CondLabel == "Ctrl":
            EngF.write("file 'Eng_TopoProj_%s.mov'\n" % (VCtrl[count_Ctrl]))
            AslF.write("file 'ASL_TopoProj_%s.mov'\n" % (VCtrl[count_Ctrl]))
            count_Ctrl += 1
        if CondLabel == "NULL":
            for i in range(int(Dur)):
                EngF.write("file 'NULL.mov'\n")
                AslF.write("file 'NULL.mov'\n")
        if CondLabel not in Conds and CondLabel not in RConds:
            print "-------Unexpected Cond Label: %s-------" % CondLabel
            with open("_ERROR", "a") as err:
                err.write("%s has Unexpected Cond Label on line %d\n" % (Par_NoExt, count_par + 1))
        count_par += 1
    EngF.close()
    AslF.close()
    count_Resp = count_RProj + count_RTopo + count_RCtrl
    count_All = count_Resp + count_Proj + count_Topo + count_Ctrl
    print "%s: %d lines converted, %d Resp items, %d Total items\n" % (ParName, count_par, count_Resp, count_All)
    #                          #number of lines converted and printed to console
def CatVids(ParName):
    Sched = ParName[-3:]
    Langs = ["ASL", "Eng"]
    for L in Langs:
        cmd = """ffmpeg -f concat -i IN_%s_%s_ALL.txt -codec copy Run_%s_Full.mov""" % (L, Sched, Sched)
        print cmd
        #os.system(cmd)
        time.sleep(.2)

def SplitCatList(InFi):
    PsyScVer = 1
    os.system("rm SplIn*.txt") #DEL existing
    for line in open("IN_%s.txt" % InFi):
        if line[-7] == "Y" or line[-7] == "N":
            PsyScVer += 1
            cmd = """cp %s Run_%s_%s_%s.mov""" % (line[6:-2], InFi, '{:02d}'.format(PsyScVer), line[-7])
            print cmd
            ##os.system(cmd)
            PsyScVer += 1
        if "Y" or "N" != line[-7]:
            with open("SplIn_%s_%s.txt" % (InFi, '{:02d}'.format(PsyScVer)), 'a') as MultiIn:
                MultiIn.write(line)
    #PsyList.close()
    print PsyScVer
def CatSplitVids(InFi):
    SpInFi = glob.glob("SplIn_*.txt")
    for elem in SpInFi:
        InNum = elem[-6:-4]
        cmd = """ffmpeg -f concat -i %s -codec copy Run_%s_%s.mov""" % (elem, InFi, InNum)
        print cmd
        #os.system(cmd)
def main():
    for elem in Par_NoExt:
        MakeCatList("%s" % elem)
    #    CatVids("%s" % elem)
    #for elem in InFi_NoExt:
    #    if elem[-3:] in SplitSched:
    #        SplitCatList("%s" % (elem))
    #        CatSplitVids("%s" % (elem))
main()

##Unused
    #for num in range(1, 21):
    #    Sched = '{:03d}'.format(num)
    #Seed = randint(100,999)
    #VRProj = {'04':'04_Y', '07':'07_N', '12':'12_Y', '14':'14_Y', '17':'17_N'}
    #VRTopo = {'25':'25_N', '29':'29_N', '32':'32_N', '39':'39_Y', '41':'41_Y'}
    #VRCtrl = {'52':'52_Y', '56':'56_N', '60':'60_N', '63':'63_Y', '65':'65_Y'}