from run import main, get_tech_type, FCIDs

def test_by_machine(capsys):
    main(query="K12345", by_machine=True)
    outerr = capsys.readouterr()
    assert outerr.out  == "HiSeq 3000,HiSeq 4000\n"

def test_by_flowcell():
    print(get_tech_type("22C37GLT3", FCIDs))
    assert get_tech_type("22C37GLT3", FCIDs)[0][0] == "NovaSeq X"

def test_by_flowcell_weird_zeros():
    assert get_tech_type("000000000-BLW8J", FCIDs)[0] == ["MiSeq"]

def test_given_patterns():
    # here I have tried to list the pattern provided by illumina tech support
    templates = {
        "xxxxxBCxx": ["HiSeq 2500", " rapid v2"],
        "xxxxxACxx": ["HiSeq 2500", " TruSeq v3"],
        "xxxxxANxx": ["HiSeq 2500", " High Output v4"],
        "xxxxxBBxx": ["HiSeq 3000", "/4000"],
        "xxxxxALxx": ["HiSeq X"],
        "xxxxxCCxx": ["HiSeq X"],
        "xxxxxDRxx": ["NovaSeq", "SP,S1"],
        "xxxxxDMxx": ["NovaSeq", "S2"],
        "xxxxxDSxx": ["NovaSeq", "S4"],
        "xxxxxAFxx": ["NextSeq 500", "/550] Mid Output"],
        "xxxxxAGxx": ["NextSeq 500", "/550 High Output"],
        "xxxxxBGxx": ["NextSeq 500", "/550 High Output"],
        "XXXXXXLT3": ["NovaSeq X"],
 	"BNTxxxxx-xxxx":["iSeq 100"],
 	"BPLxxxxx-xxxx":["iSeq 100"],
 	"000Hxxxxx": ["MiniSeq"],
 	"Dxxxx": ["MiSeq"],
 	"Gxxxx": ["MiSeq"],
 	"Lxxxx": ["MiSeq"],
        "xxxxxAFxx": ["NextSeq 500"],
        "xxxxxAGxx":["NextSeq 500"],
 	"xxxxxBGxx": ["NextSeq 500"],
        "xxxxxxxM5": ["NextSeq 1000"],
        "xxxxxxxM5": ["NextSeq 1000"],
        "xxxxxxxHV": ["NextSeq 1000"],
        "xxxxxBCxx": ["HiSeq 2500"],
        "xxxxxACxx": ["HiSeq 2500"],
        "xxxxxANxx": ["HiSeq 2500"],
        "xxxxxBBxx": ["HiSeq 3000"],
        "xxxxxCCxx": ["HiSeq X"],
        "xxxxxALxx": ["HiSeq X"],
        "xxxxxDRxx": ["NovaSeq 6000"],
        "xxxxxDMxx": ["NovaSeq 6000"],
        "xxxxxDSxx": ["NovaSeq 6000"],
        "xxxxxxLTx": ["NovaSeq X"]
        }
    for k,v in templates.items():
        res = get_tech_type(k.upper(), FCIDs)
        print(res)
        # check machine
        assert res[0][0] == v[0]
        # check chemistry
        # TODO
