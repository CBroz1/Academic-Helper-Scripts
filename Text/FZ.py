#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Chris
# @Date:   2017-3-1 14:49:37
# @Last Modified by:   CBroz1
# @Last Modified time: 2023-03-17 15:47:41

# 2023 modification: black formatted

QuestIntro = 6
QuestMC = 39
QuestSet = 6
DBugDefault = 0

import glob, csv, sys, linecache, os, argparse
from ast import literal_eval as make_tuple


class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith("R|"):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def StartUp():
    parser = argparse.ArgumentParser(
        description="Generate match percent for Friendzone users.",
        epilog="""
        1 for percents, add 2 to refresh users, add 4 to refresh questions, 8 get dist
        """,
        formatter_class=SmartFormatter,
    )
    parser.add_argument(
        "Ver",
        metavar="Version",
        type=int,
        help="Project version number, integer. Matches Matrix and data numbers.",
    )
    parser.add_argument(
        "GoLvl",
        metavar="WhatDo",
        type=int,
        help="Sum of things to do. 1 Percent. 2 Usr file. 4 Tup. 8 Distance",
    )
    parser.add_argument(
        "TUser",
        metavar="TargetUser",
        type=int,
        help="User number in database for generating percentages. Use 0 for ALL.",
    )
    parser.add_argument(
        "--dbug",
        metavar="Debug_level",
        type=int,
        default=DBugDefault,
        help="Debug level 0 to 3",
    )
    args = parser.parse_args()
    # Set Vars
    global Ver, GoLvl, TUser, DBug, GoPerc, GoUsr, GoTup, GoDist
    Ver = args.Ver
    GoLvl = args.GoLvl
    TUser = args.TUser
    GoString = " "
    DBug = args.dbug
    MaxDBug = 3
    #
    GoPerc = GoLvl & 1
    if GoPerc == 1:
        GoString += "Calculating Percents.\n"
    GoUsr = (GoLvl & 2) / 2
    if GoUsr == 1:
        GoString += " Generating User Files.\n"
    GoTup = (GoLvl & 4) / 4
    if GoTup == 1:
        GoString += " Generating Matrix Files.\n"
    GoDist = (GoLvl & 8) / 8
    if GoDist == 1:
        GoString += " Calculating Distances.\n"
    DebugDict = {0: " No Debug.", 1: " Min Debug.", 2: " Mod Debug.", 3: " Hi  Debug."}
    if DBug > MaxDBug:
        DBug = MaxDBug
    GoString += DebugDict[DBug]
    #
    print(GoString)
    choice = raw_input("Look Good? y/n")
    if choice.lower() == "n":
        sys.exit(0)
    print("--> Continued")


StartUp()


def CompileMatrix():  # matrix to tup file
    #   Personality 1, Friend Style 2, Moral/Politics 4, Lifestyle   8
    RespNum = 1
    with open("FZ_Matrix_V%02d.csv" % Ver, "rU") as csvfile:  # Added, 'rU'
        MatrixDB = csv.reader(
            csvfile, delimiter=",", quotechar='"', dialect=csv.excel_tab
        )
        next(MatrixDB, None)  # skip the header
        TupF = open("FZ_Tup_V%02d.txt" % (Ver), "w+")  # overwrites existing
        for row in MatrixDB:
            # print row
            if row[2][0] == "Q":  # If question row
                RespNum = int(row[3])  # store number of responses
                QuestionInfo = ";".join(
                    row[2:7]
                )  # Join Q_id, #resp, MaxVal, weight, category
                TupF.write("%s" % QuestionInfo)  # write to tup file
            if row[2][0] != "Q" and RespNum > 0:  # If resp row
                TupItem = row[3]  # declare response string
                for p in row[4:]:
                    if p == "FALSE":
                        TupItem += ", %s" % p  # append string 'false'
                    try:
                        int(p)
                        TupItem += ", %s" % p
                    except:
                        pass
                # print TupItem                          # for debug
                TupF.write(";(%s)" % TupItem)  # write response string to Tup file
                RespNum -= 1
            if RespNum == 0:
                TupF.write("\n")
        TupF.close()


def GenUserFiles():  # Strips responses from google form csv, to full and MC only file, sensitive to google form changes
    UserNum = 1
    with open("FZ_Data_V%02d.csv" % Ver, "rb") as csvfile:
        UserDB = csv.reader(csvfile, delimiter=",", quotechar='"')
        next(UserDB, None)  # skip the header
        for row in UserDB:  # Codebelow HARDCODED for survey structure
            CountMCResp = 0
            UsrFile_Al = open(
                "U%03d.txt" % (UserNum), "w+"
            )  # W+ truncates to 0, permits read
            UsrFile_MC = open(
                "MC_U%03d.txt" % (UserNum), "w+"
            )  # W+ truncates to 0, permits read
            for i in range(0, QuestIntro):  # Initial Qs
                UsrFile_Al.write("%s\n" % (row[i]))
            for i in range(QuestIntro, QuestIntro + QuestMC):  # MC
                try:
                    CountMCResp += 1
                    UsrFile_Al.write("%s\n" % (row[i][0]))
                    UsrFile_MC.write("%s\n" % (row[i][0]))
                except Exception, e:
                    UsrFile_Al.write("FALSE\n")
                    UsrFile_MC.write("FALSE\n")
                    if DBug != 0:
                        print(
                            "User Error: %03d Row %d Q%02d %s\n\t%s"
                            % (UserNum, i, CountMCResp, e, row[i - 1 : i + 2])
                        )
                    else:
                        continue
            for i in range(
                QuestIntro + QuestMC, QuestIntro + QuestMC + QuestSet
            ):  # Bio
                UsrFile_Al.write("%s\n" % (row[i]))
            print(
                "User Coded: %03d for %s, %d MC resp" % (UserNum, row[1], CountMCResp)
            )
            if CountMCResp != QuestMC:
                print("Error, %s had %d Questions" % (UserNum, CountMCResp))
            UsrFile_Al.close()
            UsrFile_MC.close()
            UserNum += 1


def CurlDist(Zip1, Zip2):
    UserFullFiles = glob.glob("U*.txt")
    apiFileType = "csv"  # or json
    apiKey = "KEY_HERE"
    apiURL = "https://www.zipcodeapi.com/rest/%s/distance.%s/" % (apikey, apiFileType)
    cmd = "curl %s%s/%s/mile > LocalFile.txt" % (apiURL, Zip1, Zip2)
    print(cmd)
    # os.system(cmd)
    # Then append Localfile to FZ_Dist_


def MatchPer(User):  # for specified user, get all match percents
    UserMCFiles_Ext = glob.glob("MC_U*.txt")
    UserFiles = [x.strip("MC_U").strip(".txt") for x in UserMCFiles_Ext]
    TargU_NewLine = open("MC_U%03d.txt" % User).readlines()
    TargU = [x.strip("\n") for x in TargU_NewLine]  # TargU = targ user response as list
    for AltUFile in UserFiles:  # for each other user
        MatchSum = 0.0
        MatchCount = 0.0
        PersSum = 0.0
        PersCount = 0.0
        FrieSum = 0.0
        FrieCount = 0.0
        MoraSum = 0.0
        MoraCount = 0.0
        LifeSum = 0.0
        LifeCount = 0.0
        progressSum = []  # For debug
        progressCount = []
        AltU_NewLine = open(
            "MC_U%s.txt" % AltUFile
        ).readlines()  # AltU = other user responses as list
        AltU = [x.strip("\n") for x in AltU_NewLine]
        for i in range(0, QuestMC - 1):
            TargVal = ord(TargU[i].lower()) - 96
            AltVal = ord(AltU[i].lower()) - 96
            Question = (
                linecache.getline("FZ_Tup_V%02d.txt" % Ver, i + 1)
                .strip("\n")
                .split(";")
            )  # Get Question as list
            QuestionNum = Question[0]
            MaxValForQuest = float(Question[2])
            Multiplier = float(Question[3])
            QuestType = int(Question[4])
            try:  # skips false
                # TupFile structure:  ('Qxx', NumResp, MaxVal, Multiplier, (aa, ab, ac, ad), (ba, bb, bc, bd), (ca, cb, cc, cd), (da, db, dc, dd))
                OrdinalVal = float(make_tuple(Question[TargVal + 4])[AltVal - 1])
                if OrdinalVal == 0:
                    continue
                MatchVal = 1 - ((OrdinalVal - 1) * 1 / float(MaxValForQuest))
                MatchSum += MatchVal * Multiplier
                MatchCount += Multiplier
                #   Personality 1, Friend Style 2, Moral/Politics 4, Lifestyle   8
                if (QuestType & 1) == 1:
                    PersSum += MatchVal * Multiplier
                    PersCount += Multiplier
                if (QuestType & 2) == 2:
                    FrieSum += MatchVal * Multiplier
                    FrieCount += Multiplier
                if (QuestType & 4) == 4:
                    # print "%s is moral" % QuestionNum
                    MoraSum += MatchVal * Multiplier
                    MoraCount += Multiplier
                    # print "Moral count %d, Mult %d" % (MoraCount, Multiplier)
                if (QuestType & 5) == 5:
                    # print "%s is life" % QuestionNum
                    LifeSum += MatchVal * Multiplier
                    LifeCount += Multiplier

                # Debug stuff
                ExplicitString = (
                    "%s Targ %s %r Alt %s %r Ord %r Max %r Match %.2f Mult %r"
                    % (
                        QuestionNum,
                        TargU[i],
                        TargVal,
                        AltU[i],
                        AltVal,
                        OrdinalVal,
                        MaxValForQuest,
                        MatchVal,
                        Multiplier,
                    )
                )
                if DBug >= 3:
                    print("   %s" % (ExplicitString))
                MatchSumRounded = "{0:.2f}".format(MatchSum)
                progressSum.append(MatchSumRounded)
                progressCount.append(MatchCount)
            except Exception, e:
                if DBug == 0:
                    pass
                if DBug >= 1:
                    print("Er %s %s" % (ExplicitString, e))
                if DBug >= 2:
                    RecentAddedSum = float(progressSum[-1]) - float(progressSum[-2])
                    RecentAddedMult = float(progressCount[-1]) - float(
                        progressCount[-2]
                    )
                    print(
                        "Added Val*Mult %.2f Added Mult %r"
                        % (RecentAddedSum, RecentAddedMult)
                    )
        # moved indent back one
        MatchPercent = float(MatchSum / MatchCount)
        PersPercent = float(PersSum / PersCount)
        FriePercent = float(FrieSum / FrieCount)
        MoraPercent = float(MoraSum / MoraCount)
        LifePercent = float(LifeSum / LifeCount)
        TargU_id = linecache.getline("U%03d.txt" % User, 2).strip(
            "\n"
        )  # Get user id from full user file
        AltU_id = linecache.getline("U%s.txt" % AltUFile, 2).strip("\n")
        print(
            "%s, %s: %.3f, Pers %.3f, Frie %.3f, Mora %.3f, Life %.3f"
            % (
                TargU_id,
                AltU_id,
                float(MatchPercent),
                PersPercent,
                FriePercent,
                MoraPercent,
                LifePercent,
            )
        )
        SetCounts(User, int(AltUFile))


def SetCounts(TUser, AUser):
    SetStart = QuestIntro + QuestMC
    SetOutput = "     Hob, bk, gam, mov, spt, mus: "
    for i in range(1, QuestSet + 1):
        TUserList = (
            linecache.getline("U%03d.txt" % TUser, SetStart + i).strip("\n").split(",")
        )
        AUserList = (
            linecache.getline("U%03d.txt" % AUser, SetStart + i).strip("\n").split(",")
        )
        CommoList = set(TUserList) & set(AUserList)
        LenString = "%d, " % len(CommoList)
        SetOutput += LenString
    print(SetOutput[:-2])


def main():
    if GoTup == 1:
        CompileMatrix()
    if GoUsr == 1:
        GenUserFiles()
    if GoPerc == 1:
        if TUser == 0:
            UserMCFiles_Ext = glob.glob("MC_U*.txt")
            UserFiles = [x.strip("MC_U").strip(".txt") for x in UserMCFiles_Ext]
            MaxUser = int(UserFiles[-1])
            print("Total Users: %d" % MaxUser)
            for num in range(1, MaxUser + 1):
                MatchPer(num)
        else:
            MatchPer(TUser)


main()

# ---------------------------------#
