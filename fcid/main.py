import re
import sys


InstrumentIDs = [
    ["HWI-M[0-9]{4}$", [["MiSeq"]]],
    ["HWUSI", [["Genome Analyzer IIx"]]],
    ["M[0-9]{5}$",  [["MiSeq"]]],
    ["HWI-C[0-9]{5}$",  [["HiSeq 1500"]]],
    ["C[0-9]{5}$",  [["HiSeq 1500"]]],
    ["HWI-D[0-9]{5}$",  [["HiSeq 2500"]]],
    ["D[0-9]{5}$",  [["HiSeq 2500"]]],
    ["J[0-9]{5}$",  [["HiSeq 3000"]]],
    ["K[0-9]{5}$",  [["HiSeq 3000", "HiSeq 4000"]]],
    ["E[0-9]{5}$",  [["HiSeq X"]]],
    ["NB[0-9]{6}$",  [["NextSeq"]]],
    ["NS[0-9]{6}$",  [["NextSeq"]]],
    ["MN[0-9]{5}$",  [["MiniSeq"]]],
    ["A[0-9]{5}$",  [["NovaSeq"]]],
    ["NA[0-9]{5}$",  [["NovaSeq"]]],
    ["SN[0-9]{3}$",  [["HiSeq2000", "HiSeq2500"]]],
    ["SN[0-9]{3}$",  [["HiSeq2000", "HiSeq2500"]]],
    [".*",  [["Unknown"]]]
]
FCIDs = [
    ["^C[A-Z,0-9]{4}ANXX$",   [["HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v4 flow cell"]],
    ["^C[A-Z,0-9]{4}AC[A-Z,0-9]{2}$",   [["HiSeq 2500"], "High Output (8-lane) v4 flow cell"]],
    ["^C[A-Z,0-9]{4}ACXX$",   [["HiSeq 1000", "HiSeq 1500", "HiSeq 2000", "HiSeq 2500"], "High Output (8-lane) v3 flow cell"]],
    ["^C[A-Z,0-9]{4}AC[A-Z,0-9]{2}$",   [["HiSeq 2500"], "TrueSeq  v3 flow "]],
    ["^H[A-Z,0-9]{4}ADXX$",   [["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v1 flow cell"]],
    ["^H[A-Z,0-9]{4}ADXY$",   [["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v1 flow cell"]],
    ["^H[A-Z,0-9]{4}BCXX$",   [["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"]],
    ["^H[A-Z,0-9]{4}BCXY$",   [["HiSeq 1500", "HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"]],
    ["^H[A-Z,0-9]{4}BC[A-Z,0-9]{2}$",   [["HiSeq 2500"], "Rapid Run (2-lane) v2 flow cell"]],
    ["^H[A-Z,0-9]{4}BBXX$",   [["HiSeq 4000"], "(8-lane) v1 flow cell"]],
    ["^H[A-Z,0-9]{4}BBXY$",   [["HiSeq 4000"], "(8-lane) v1 flow cell"]],
    ["^H[A-Z,0-9]{4}BBXY[A-Z,0-9]{2}$",   [["HiSeq 4000"], "(8-lane) v1 flow cell"]],
    ["^H[A-Z,0-9]{4}CCXX$",   [["HiSeq X"], "(8-lane) flow cell"]],
    ["^H[A-Z,0-9]{4}CCXY$",   [["HiSeq X"], "(8-lane) flow cell"]],
    ["^H[A-Z,0-9]{4}AL[A-Z,0-9]{2}$",   [["HiSeq X"], "(8-lane) flow cell"]],
    ["^H[A-Z,0-9]{4}BGXX$",   [["NextSeq"], "High output flow cell"]],
    ["^H[A-Z,0-9]{4}BGXY$",   [["NextSeq"], "High output flow cell"]],
    ["^H[A-Z,0-9]{4}BG[A-Z,0-9]{2}$",   [["NextSeq"], "High output flow cell"]],
    ["^H[A-Z,0-9]{4}AF[A-Z,0-9]{2}$",   [["NextSeq"], "Mid output flow cell"]],
    ["^A[A-Z,0-9]{4}$",   [["MiSeq"], "MiSeq flow cell"]],
    ["^B[A-Z,0-9]{4}$",   [["MiSeq"], "MiSeq flow cell"]],
    ["^D[A-Z,0-9]{4}$",   [["MiSeq"], "MiSeq nano flow cell"]],
    ["^G[A-Z,0-9]{4}$",   [["MiSeq"], "MiSeq micro flow cell"]],
    ["^H[A-Z,0-9]{4}DM[A-Z,0-9]{2}$",   [["NovaSeq"], "S2 flow cell"]],
    ["^H[A-Z,0-9]{4}DR[A-Z,0-9]{2}$",   [["NovaSeq"], "SP or S1 flow cell"]],
    ["^H[A-Z,0-9]{4}DS[A-Z,0-9]{2}$",   [["NovaSeq"], "S4 flow cell"]],
    ["^[A-Z0-9]{6}LT3$",   [["NovaSeq X"], "(10B)"]],
    ["^C[A-Z,0-9]{4}$",   [["MiSeq"], "MiSeq flow cell"]],
    ["^J[A-Z,0-9]{4}$",   [["MiSeq"], "MiSeq flow cell"]],
    ["^K[A-Z,0-9]{4}$",   [["MiSeq"], "MiSeq flow cell"]],
    [".*",  [["Unknown Machine"], "Unknown flowcell"]
     ]
]


def get_tech_type(flowcell, d):
    for pattern, value in d:
        if re.search(pattern, flowcell):
            return value
    return None

def main(query, by_machine=False):
    if by_machine:
        res = get_tech_type(query, InstrumentIDs)
    else:
        res = get_tech_type(query, FCIDs)
    sys.stdout.write(",".join(res[0]) + "\n")

if False: # some tests
    main(query="CABBCANXX")
    main(query="KSQURL", by_machine=True)
    get_flowcell_type("22C37GLT3", FCIDs)

def cli():
    args = sys.argv[1:]
    by_machine = False
    if "--by-machine" in args:
        by_machine=True
        args.remove("--by-machine")
    if len(args) != 1:
        raise ValueError ("USAGE: fcid <flowcell|machine> [--by-machine]")
    main(query=args[0], by_machine=by_machine)
