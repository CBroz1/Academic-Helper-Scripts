# -*- coding: utf-8 -*-
# @Author: ChrisBrozdowski
# @Date:   2020-06-22 22:55:56
# @Last Modified by:   local-admin
# @Last Modified time: 2020-06-27 09:21:14

##NOTES
	# Gets experimental list that feed AmToCS experiment
	# randomizes until alternating pattern
	# saves with 'testing' marker
	# when packaged with PyInstaller launch AmToCS eprime

import random, os 
	# random for shuffle
	#os for exec command
import time # for log file
localtime = time.asctime( time.localtime(time.time()) )

Testing = ""	# blank when not testing
				# adds file suffix for testing and limits cycles

def scramble(Subtest):
	with open('StimLists/%sExp.txt' % Subtest, 'r') as SubtestFile:
		## open to read existing
		SubtestList = [line.strip() for line in SubtestFile] #file to list
		SubtestHead = SubtestList[0]						 #file header
		SubtestList = SubtestList[1:]						 #file contents
	SubtestGend = [0, 0, 1]							# dummy for failing while loop
	while not alternating(SubtestGend):				# while Gender not Alternating
		random.shuffle(SubtestList)					# Randomize list
		SubtestGend = [ ]							# empty Gender
		SubtestItem = [ ]
		for line in SubtestList:					# loop list, get gender
			SubtestLine = line.split('\t')			# split string by tab
			SubtestGend.append(SubtestLine[7:8][0][0]) #7th col, 1st item, 1st char
			SubtestItem.append(SubtestLine[3])
	print(Subtest, SubtestGend)						# print Gend to console
	with open('StimLists/%sExp%s.txt' % (Subtest, Testing), 'w') as SubtestFile:
		SubtestFile.write('%s\n' % SubtestHead) 	# write new file header
		for item in SubtestList:					# write randomize contents
			SubtestFile.write('%s\n' % item)
	with open('StimLists/zLogFile.txt', 'a') as LogFile:
		LogLine = localtime + " " + Subtest + " " + ', '.join(SubtestItem) 
		LogFile.write('%s\n' % LogLine) 						# write time, subtest, item list
		if Subtest == "Para": LogFile.write('\n') 

# This is the constraint we're checking against in specific column. Could be anything.
def alternating(l):									# check alternating T/f
    for i in range(len(l)-2):						# code pulled from StackOverflow forum post
        if (l[i] < l[i+1]) and (l[i+1] > l[i+2]):
            continue
        if (l[i] > l[i+1]) and (l[i+1] < l[i+2]):
            continue
        return False
    return True

## https://stackoverflow.com/questions/38969629/program-to-check-if-list-is-in-alternating-form

def main():
	if Testing == "":
		SubtestArray = ["Word", "Sent", "Para"]
	else:
		SubtestArray = ["Para"]
	for Subtest in SubtestArray:
		scramble(Subtest)
	WinCmd = "copy StimLists\\*txt ..\\..\\StimLists\\ /y & ..\\..\\AmToCS.ebs3"
		# copies txt files with /y for default overwrite
		# must use \\ for literal \ in python
		# OSX cmd would look differnt, use unix
	os.system(WinCmd) 	  		# Windows 
	
main()

#pyinstaller notes
	# use python.org installer, not windows store
	# pyinstaller runs and generates dist folder where app must live
	# build folder and other files don't seem to do anything
	# app that works on other files must also copy files to where they're later expected to be
	#	see WinCmd above for copying files