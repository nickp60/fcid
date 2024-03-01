import re
import sys


InstrumentIDs = [
    ["HWI-M[0-9]{4}", [["MiSeq"]]],
    ["HWUSI", [["Genome Analyzer IIx"]]],
    ["M[0-9]{5}",  [["MiSeq"]]],
    ["HWI-C[0-9]{5}",  [["HiSeq 1500"]]],
    ["C[0-9]{5}",  [["HiSeq 1500"]]],
    ["HWI-D[0-9]{5}",  [["HiSeq 2500"]]],
    ["D[0-9]{5}",  [["HiSeq 2500"]]],
    ["J[0-9]{5}",  [["HiSeq 3000"]]],
    ["K[0-9]{5}",  [["HiSeq 3000", "HiSeq 4000"]]],
    ["E[0-9]{5}",  [["HiSeq X"]]],
    ["NB[0-9]{6}",  [["NextSeq"]]],
    ["NS[0-9]{6}",  [["NextSeq"]]],
    ["MN[0-9]{5}",  [["MiniSeq"]]],
    ["A[0-9]{5}",  [["NovaSeq"]]],
    ["NA[0-9]{5}",  [["NovaSeq"]]],
    ["SN[0-9]{3}",  [["HiSeq2000", "HiSeq2500"]]],
    ["SN[0-9]{3}",  [["HiSeq2000", "HiSeq2500"]]],
    [".*",  [["Unknown"]]]
]
# Below ar ethe relevant texts from the 3 emails with tech support
# ------------------------------------
# xxxxxBCxx: HiSeq 2500 rapid v2
# xxxxxACxx: HiSeq 2500 TruSeq v3
# xxxxxANxx: HiSeq 2500 High Output v4
# xxxxxBBxx: HiSEQ 3000/4000
# xxxxxALxx; xxxxxCCxx: HiSeqX
#
# xxxxxDRxx: NovaSeq SP,S1
# xxxxxDMxx: NovaSeq S2
# xxxxxDSxx: NovaSeq S4
#
# xxxxxAFxx: NextSeq 500/550 Mid Output
# xxxxxBGxx; xxxxxAGxx: NextSeq 500/550 High Output
#--------------------------------------
#  I believe the format for 10B NovaSeq X cells will be "XXXXXXLT3". The 1.5B and 25B cells will likely use a different format
#---------------------------------------
# iSeq 100 	BNTxxxxx-xxxx (BRB/BPC/BPG/BPA/BPL/BNT/BTR)
# MiniSeq Mid Output 	000Hxxxxx
# MiniSeq High Output 	000Hxxxxx
# MiSeq Nano 	Dxxxx
# MiSeq Micro 	Gxxxx
# MiSeq Standard 	Bxxxx; Cxxxx; Jxxxx; Kxxxx; Lxxxx
# NextSeq 500/550 Mid Output 	xxxxxAFxx
# NextSeq 500/550 High Output 	xxxxxBGxx; xxxxxAGxx
# NextSeq 1000/2000 P1  	xxxxxxxM5
# NextSeq 1000/2000 P2 	xxxxxxxM5
# NextSeq 2000 P3 	xxxxxxxHV
# HiSeq 2500 Rapid v2 	xxxxxBCxx
# HiSeq 2500 TruSeq v3 	xxxxxACxx
# HiSeq 2500 High Output v4 	xxxxxANxx
# HiSeq 3000/4000  	xxxxxBBxx
# HiSeq X 	xxxxxALxx; xxxxxCCxx
# NovaSeq 6000 SP and S1 	xxxxxDRxx
# NovaSeq 6000 S2 	xxxxxDMxx
# NovaSeq 6000 S4 	xxxxxDSxx
# NovaSeq X/X Plus 10B 	xxxxxxLTx


# Three emails: 12/7/2022, 9/19/2023, and 2/29/2024
FCIDs = [
    ["BNT[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["BRB[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["BPC[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["BPG[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["BPA[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["BPL[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["BNT[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["BTR[A-Z,0-9]{5}-[A-Z,0-9]{4}", [["iSeq 100"], "Standard Output flow cell"]],
    ["000H[A-Z,0-9]{5}", [["MiniSeq"], "Mid or High Output flow cell"]],
    ["D[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Nano flow cell"]],
    ["G[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Micro flow cell"]],
    ["A[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Standard v2 flow cell"]],
    ["B[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Standard flow cell"]],
    ["C[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Standard flow cell"]],
    ["J[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Standard flow cell"]],
    ["K[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Standard flow cell"]],
    ["L[A-Z,0-9]{4}",   [["MiSeq"], "MiSeq Standard flow cell"]],
    ["[A-Z,0-9]{5}AF[A-Z,0-9]{2}",   [["NextSeq 500", "NextSeq 550"], "Mid Output flow cell"]],
    ["[A-Z,0-9]{5}AG[A-Z,0-9]{2}",   [["NextSeq 500", "NextSeq 550"], "High Output flow cell"]],
    ["[A-Z,0-9]{5}BG[A-Z,0-9]{2}",   [["NextSeq 500", "NextSeq 550"], "High Output flow cell"]],
    ["[A-Z,0-9]{7}M5",   [["NextSeq 1000", "NextSeq 2000"], "P1 or P2 flow cell"]],
    ["[A-Z,0-9]{7}HV",   [["NextSeq 1000", "NextSeq 2000"], "P3 flow cell"]],

    ["H[A-Z,0-9]{4}BGXX",   [["NextSeq"], "High output flow cell"]],
    ["H[A-Z,0-9]{4}BGXY",   [["NextSeq"], "High output flow cell"]],

    ["[A-Z,0-9]{5}BC[A-Z,0-9]{2}",   [["HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"]],
    ["[A-Z,0-9]{5}AC[A-Z,0-9]{2}",   [["HiSeq 2500"], "TrueSeq v3 flow cell"]],
    ["[A-Z,0-9]{5}AN[A-Z,0-9]{2}",   [["HiSeq 2500"], "High Output v3 flow cell"]],
    ["[A-Z,0-9]{5}BB[A-Z,0-9]{2}",   [["HiSeq 3000", "HiSeq 4000"], "(8-lane) v1 flow cell"]],
    ["[A-Z,0-9]{5}AL[A-Z,0-9]{2}",   [["HiSeq X"], "(8-lane) flow cell"]],
    ["[A-Z,0-9]{5}CC[A-Z,0-9]{2}",   [["HiSeq X"], "(8-lane) flow cell"]],
    ["[A-Z,0-9]{5}DR[A-Z,0-9]{2}",   [["NovaSeq 6000"], "SP or S1 flow cell"]],
    ["[A-Z,0-9]{5}DM[A-Z,0-9]{2}",   [["NovaSeq 6000"], "S2 flow cell"]],
    ["[A-Z,0-9]{5}DS[A-Z,0-9]{2}",   [["NovaSeq 6000"], "S4 flow cell"]],
    ["[A-Z0-9]{6}LT[A-Z,0-9]",   [["NovaSeq X", "NovaSeq X Plus"], "10B flow cell"]],

#    ["[A-Z,0-9]{5}ACXX",   [["HiSeq 1000", "HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v3 flow cell"]],
#    ["H[A-Z,0-9]{4}BCXY",   [["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"]],
#    ["C[A-Z,0-9]{4}ANXX",   [["HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v4 flow cell"]],
#    ["C[A-Z,0-9]{4}AC[A-Z,0-9]{2}",   [["HiSeq 2500"], "High Output (8-lane) v4 flow cell"]],
#    ["H[A-Z,0-9]{4}ADXX",   [["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v1 flow cell"]],
#    ["H[A-Z,0-9]{4}ADXY",   [["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v1 flow cell"]],
#    ["H[A-Z,0-9]{4}BC[A-Z,0-9]{2}",   [["HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"]],
#    ["H[A-Z,0-9]{4}BBXY[A-Z,0-9]{2}",   [["HiSeq 4000"], "(8-lane) v1 flow cell"]],
    [".*",  [["Unknown Machine"], "Unknown flowcell"]
     ]
]


def get_tech_type(flowcell, d):
    flowcell = flowcell.replace("000000000-", "")
    for pattern, value in d:
        if re.search("^" + pattern + "$", flowcell):
            return value
    return None

def main(query, by_machine=False):
    if by_machine:
        res = get_tech_type(query, InstrumentIDs)
    else:
        res = get_tech_type(query, FCIDs)
    sys.stdout.write(",".join(res[0]) + "\n")


def cli():
    args = sys.argv[1:]
    by_machine = False
    if "--by-machine" in args:
        by_machine=True
        args.remove("--by-machine")
    if len(args) != 1:
        raise ValueError ("USAGE: fcid <flowcell|machine> [--by-machine]")
    main(query=args[0], by_machine=by_machine)
