# @Last Modified by:   cb
# @Last Modified time: 2020-02-19 19:38:35

# what it do: Get list xmat files. Run 3dCon_DeC for each NoiseVal

import glob, os  # importing glob for listing files

XmatFiles = glob.glob(
    "*[0-9].xmat.1D"
)  # List all .xmat files (notXtXiv) in current dir
Scheds = [i.split(".")[0] for i in XmatFiles]  # Sched name only
NoiseVals = [0, 1, 2]  # Noise Levels
ModelVals = ["WAV", "SPMG2"]  # Models Tested


def main():
    for f in Scheds:  # For every xmat file in dir
        for n in NoiseVals:
            for m in ModelVals:
                cmd = f"../../_Scripts/Con_DeCon.sh {f} {n} {m}"
                print(cmd)
                # os.system(cmd)


main()
