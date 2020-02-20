# -*- coding: utf-8 -*-
# @Author: christopherbrozdowski
# @Date:   2017-04-26 12:54:38
# @Last Modified by:   christopherbrozdowski
# @Last Modified time: 2017-05-01 16:51:15

import glob, csv, sys, linecache, os, argparse
from ast import literal_eval as make_tuple

def StartUp():
	parser = argparse.ArgumentParser(
		description='Generate input files for ffmpeg concatenate in Shadowing Experiment.',
		epilog="SelfFirst: 1-1, 3-1, 5-0, 7-0, 9-1, 11-0, 13-1, 15-0, 17-1, 19-0")
	parser.add_argument('Group', metavar='Group_HorD', type=str,
	                    help='Group Identity, H for Hearing, D for Deaf')
	parser.add_argument('Subj', metavar='SubjectNumber', type=int,
	                    help='Subject Number, Lower of Pair, Should be Odd')
	parser.add_argument('SelfFirst', metavar='Self_Friend', type=int,
	                    help='Self first or Friend first. Self=1, Friend=0')
	parser.add_argument('MakeVids', metavar='Make_Vids', type=int,
	                    help='Run the ffmpeg command to run vids. Yes=1, Dry Run=0')
	args = parser.parse_args()
#Set Vars	
	global Group, Subj1, Subj2, SelfFirst, Conds, Pre, EndSt, EndBr, MakeVids
	Group = args.Group
	Subj1 = int(args.Subj)
	Subj2 = Subj1 + 1
	SelfFirst = args.SelfFirst
	if SelfFirst == 1:
		SelfFirst_Str = 'Self First'
	if SelfFirst == 0:
		SelfFirst_Str = 'Friend First'
	else:
		SelfFirst_Str = 'STOP IT'
	MakeVids = args.MakeVids
	if int(MakeVids) == 1:
		MakeVids_Str = 'Running ffmpeg'
	if int(MakeVids) == 0:
		MakeVids_Str = 'Dry Run'
	else:
		MakeVids_Str = 'Stop it, I\'m confused'
	Conds = ['Sign', 'Gest']
	Pre = 'file \''
	EndSt = 'file \'../Sha_Run_Stim/Sha_EndString.mov\''
	EndBr = 'file \'../Sha_Run_Stim/Sha_EndBreak.mov\''
	CounterBal = """
FilmOrder: 1-1, 3-0, 5-0, 7-0, 9-0, 11-0, 13-0, 15-0, 17-0, 19-0
TestOrder: 1-0, 3-0, 5-1, 7-1, 9-0, 11-0, 13-1, 15-0, 17-1, 19-0
WMOrder__: 1-0, 3-1, 5-1, 7-0, 9-0, 11-1, 13-1, 15-0, 17-0, 19-0
SelfFirst: 1-1, 3-1, 5-0, 7-0, 9-1, 11-0, 13-1, 15-0, 17-1, 19-0\n\n"""
#Check Inputs
	print "%s%s: %s%02d, %s%02d, %s" % (CounterBal, MakeVids_Str, Group, Subj1, Group, Subj2, SelfFirst_Str) 
	choice = raw_input("Look Good? y/n")
	if choice.lower() == "n":
	    sys.exit(0)
	print "--> Continued"
StartUp()

def BuildSelf(Con, Self, Frie):
	InFile.write("%s../Sha_Run_Stim/Sha_Hold_Self.mov\'\n" % Pre)
	SubjVid = "%sShad_%s%02d_%sL" % (Pre, Group, Self, Con[0])
	for ll in range(1, 6):
		InFile.write("%s%02d.mov\'\n%s\n" % (SubjVid, ll, EndSt))
	InFile.write("%s06.mov\'\n%s\n" % (SubjVid, EndBr))
	for ll in range(7, 12):
		InFile.write("%s%02d.mov\'\n%s\n" % (SubjVid, ll, EndSt))
	InFile.write("%s12.mov\'\n" % (SubjVid))

def BuildFriend(Con, Self, Frie):
	InFile.write("%s../Sha_Run_Stim/Sha_Hold_Friend.mov\'\n" % Pre)
	SubjVid = "%sShad_%s%02d_%sL" % (Pre, Group, Frie, Con[0])
	for ll in range(1, 6):
		# for 1-6 Shad_Group_Subj_list, EndSt
		InFile.write("%s%02d.mov\'\n%s\n" % (SubjVid, ll, EndSt))
	InFile.write("%s06.mov\'\n%s\n" % (SubjVid, EndBr))
	for ll in range(7, 12):
		InFile.write("%s%02d.mov\'\n%s\n" % (SubjVid, ll, EndSt))
	InFile.write("%s12.mov\'\n" % (SubjVid))

def BuildInFi(Con, Self, Frie):
	global InFile
	InFile = open("_in_%s%02d_%s.txt" % (Group, Self, Con), 'w+')
	InFile.write("%s../Sha_Run_Stim/Sha_Intro_%s.mov\'\n" % (Pre, Con[0]))
	if int(SelfFirst)==1:
		BuildSelf(Con, Self, Frie)
		InFile.write("%s\n" % (EndBr))
		BuildFriend(Con, Self, Frie)
	if int(SelfFirst)==0:
		BuildFriend(Con, Self, Frie)
		InFile.write("%s\n" % (EndBr))
		BuildSelf(Con, Self, Frie)
	else:
		pass # this was running when it shouldn't have.
		# print "CHECK SelfFirst Val: %s" % SelfFirst
	InFile.write("%s../Sha_Run_Stim/Sha_End%s.mov\'\n" % (Pre, Con))
	InFile.close()

def MakeRunVid(Con, Self, Frie):
	In = "_in_%s%02d_%s.txt" % (Group, Self, Con)
	Out = "Shad_Run_%s%02d_%s.mov" % (Group, Self, Con)
	#Loglevel could be error or fatal or panic
	cmd = "ffmpeg -loglevel error -y -f concat -safe 0 -i %s -codec copy -an %s" % (In, Out)
	print cmd
	if int(MakeVids) == 1:
		os.system(cmd)
	else:
		print "Didn't run"

def main():
    for Con in Conds:
    	BuildInFi(Con, Subj1, Subj2)
    	BuildInFi(Con, Subj2, Subj1)
    	MakeRunVid(Con, Subj1, Subj2)
    	MakeRunVid(Con, Subj2, Subj1)

main()