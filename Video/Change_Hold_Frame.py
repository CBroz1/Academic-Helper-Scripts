# -*- coding: utf-8 -*-
# @Author: Chris
# @Date:   2016-11-15 14:49:37
# @Last Modified by:   CB
# @Last Modified time: 2017-05-20 01:32:19


import glob, os                          #importing glob for listing files
from os import rename, listdir            

Vids = glob.glob("Sha_CB_G12*mov")                  #List all criteria files in current dir
rVids = glob.glob("r*mov")
pics = glob.glob("pic_*jpg")

FrNum = {
    'Sha_CB_G01.mov': 110,
    'Sha_CB_G02.mov': 92,
    'Sha_CB_G03.mov': 100,
    'Sha_CB_G04.mov': 141,
    'Sha_CB_G05.mov': 109,
    'Sha_CB_G06.mov': 99,
    'Sha_CB_G07.mov': 111,
    'Sha_CB_G08.mov': 105,
    'Sha_CB_G09.mov': 105,
    'Sha_CB_G10.mov': 134,
    'Sha_CB_G11.mov': 133,
    'Sha_CB_G12.mov': 126,
    'Sha_CB_S01.mov': 105,
    'Sha_CB_S02.mov': 111,
    'Sha_CB_S03.mov': 128,
    'Sha_CB_S04.mov': 127,
    'Sha_CB_S05.mov': 112,
    'Sha_CB_S06.mov': 119,
    'Sha_CB_S07.mov': 123,
    'Sha_CB_S08.mov': 98,
    'Sha_CB_S09.mov': 138,
    'Sha_CB_S10.mov': 137,
    'Sha_CB_S11.mov': 134,
    'Sha_CB_S12.mov': 141,
    'null': 11
}
WM_Lists = {
    'WM_21': [12, 6],
    'WM_22': [2, 11],
    'WM_23': [4, 8],
    'WM_31': [7, 3, 9],
    'WM_32': [4, 10, 2],
    'WM_33': [12, 6, 8],
    'WM_41': [3, 9, 1, 7],
    'WM_42': [8, 4, 11, 2],
    'WM_43': [4, 12, 5, 9],
    'WM_51': [10, 3, 12, 1, 7],
    'WM_52': [2, 7, 4, 8, 5],
    'WM_53': [11, 3, 9, 6, 10],
    'WM_61': [1, 9, 5, 12, 5, 8],
    'WM_62': [9, 1, 7, 4, 11, 2],
    'WM_63': [6, 8, 2, 10, 1, 11],
    'WM_71': [12, 5, 8, 3, 10, 6, 4],
    'WM_72': [2, 11, 3, 9, 5, 12, 1],
    'WM_73': [7, 5, 10, 6, 8, 3, 11]
}
Conds = ['S', 'G']
    
def Resize(mov): 
    cmd = """ffmpeg -i %s -vf scale=1280:720 -strict -2 r%s""" % (mov, mov)
    print cmd
    os.system(cmd)

def Rename(mov):
    cmd="""mv %s %s""" % (mov, mov[1:])
    print cmd
    os.system(cmd)

def JpgToPict(pic):
    cmd="""convert %s %s.pict""" % (pic, pic[:-4])
    print cmd
    #os.system(cmd)

def GetLast(mov):
    cmd1 = "echo %s >> z_FrameList.txt" % mov
    cmd2 = "ffprobe -loglevel panic -show_streams %s 2> /dev/null | grep nb_frames | head -1 | cut -d \= -f 2  >> z_FrameList.txt" % mov
    print cmd1
    print cmd2
    os.system(cmd1)
    os.system(cmd2)

def MakeHold(mov):
    cmd1 = "ffmpeg -loglevel panic -i %s -vf \"select='eq(n,%d)'\" -vframes 1 %s_LaFr.png" % (mov, FrNum[mov], mov[:-4])
    cmd2 = "ffmpeg -loglevel panic -loop 1 -i %s_LaFr.png -c:v libx264 -t 1 -pix_fmt yuv420p Hold_%s" % (mov[:-4], mov)
    print cmd1
    print cmd2
    os.system(cmd1)
    os.system(cmd2)
    #os.system(cmd3)

def CatHoldMakeIn(mov):
    pre = "file '"
    f = open('zIn_%s.txt' % mov[:-4], 'w')
    f.write("%s%s'\n" % (pre, mov))
    f.write("%sHold_%s'\n" % (pre, mov))
    f.close
    
def CatHold(mov):
    cmd = "ffmpeg -f concat -i zIn_%s.txt -c copy MoHo_%s" % (mov[:-4], mov)
    print cmd
    os.system(cmd)

def CatListMakeIn():
    pre = "file '"
    for Con in Conds:
        for key in WM_Lists.keys():
            #print 'zIn_%s_%s.txt' % (Con, key)
            f = open('zIn_%s_%s.txt' % (Con, key), 'w')
            for elem in WM_Lists[key][:-1]:
                #pass
                #print elem
                f.write("%sSha_CB_%s%02d.mov'\n" % (pre, Con, elem))
                f.write("%sHold_Sha_CB_%s%02d.mov'\n" % (pre, Con, elem))
            f.write("%sSha_CB_%s%02d.mov'" % (pre, Con, WM_Lists[key][-1]))
            f.close

def CatList():
    for Con in Conds:
        for key in WM_Lists.keys():
            InFi = 'zIn_%s_%s.txt' % (Con, key)
            OutFi = 'WM_%sL%s.mov' % (Con, key[-2:])
            cmd = "ffmpeg -f concat -i %s -c copy %s" % (InFi, OutFi)
            #print cmd
            os.system(cmd)

def main():
    for elem in Vids:
        #Resize(elem)
        pass
        #GetLast(elem)
        #MakeHold(elem)
        #CatHoldMakeIn(elem)
        #CatHold(elem)
    for elem in rVids:    
        #Rename(elem)
        pass
    for elem in pics:
        pass
        #JpgToPict(elem)
    #CatListMakeIn()
    CatList()

main()