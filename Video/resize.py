# -*- coding: utf-8 -*-
# @Author: Chris
# @Date:   2016-11-15 14:49:37
# @Last Modified by:   cb
# @Last Modified time: 2023-03-17 11:30:33

import glob, os                           #importing glob for listing files
from os import rename, listdir            

Vids = glob.glob("WM_*mov")                  #List all criteria files in current dir
rVids = glob.glob("rWM_*mov")
pics = glob.glob("pic_*jpg")

    
def Resize(mov): 
    cmd = """ffmpeg -i %s -vf scale=1280:720 r%s""" % (mov, mov)
    print cmd
    #os.system(cmd)

def Rename(mov):
    cmd="""mv %s %s""" % (mov, mov[1:])
    print cmd
    os.system(cmd)

def JpgToPict(pic):
    cmd="""convert %s %s.pict""" % (pic, pic[:-4])
    print cmd
    os.system(cmd)

def main():
    for elem in Vids:
        Resize(elem)
        #pass
    for elem in rVids:
        Rename(elem)
        #pass
    for elem in pics:
        pass
        #JpgToPict(elem)

main()