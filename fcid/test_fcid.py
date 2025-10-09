import subprocess
import sys

from unittest.mock import patch

from run import main, get_tech_type, FCIDs


def test_by_machine(capsys):
    testargs = ["fcid", "K12345", "--by-machine"]
    with patch.object(sys, "argv", testargs):
        main()
    outerr = capsys.readouterr()
    assert outerr.out == "HiSeq 3000,HiSeq 4000\n"

def test_by_machine_nextseq(capsys):
    testargs = ["fcid", "VH12345", "--by-machine"]
    with patch.object(sys, "argv", testargs):
        main()
    outerr = capsys.readouterr()
    assert outerr.out == "NextSeq 2000\n"


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
        "BNTxxxxx-xxxx": ["iSeq 100"],
        "BPLxxxxx-xxxx": ["iSeq 100"],
        "000Hxxxxx": ["MiniSeq"],
        "Dxxxx": ["MiSeq"],
        "Gxxxx": ["MiSeq"],
        "Lxxxx": ["MiSeq"],
        "xxxxxAFxx": ["NextSeq 500"],
        "xxxxxAGxx": ["NextSeq 500"],
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
        "xxxxxxLTx": ["NovaSeq X"],
    }
    for k, v in templates.items():
        res = get_tech_type(k.upper(), FCIDs)
        print(res)
        # check machine
        assert res[0][0] == v[0]
        # check chemistry
        # TODO


def test_by_novaseqx():
    assert get_tech_type("ABCDEFLT2", FCIDs)[0][0] == "NovaSeq X"
    assert get_tech_type("ABCDEFLT2", FCIDs)[1] == "Unknown flow cell"
    assert get_tech_type("ABCDEFLT5", FCIDs)[1] == "Unknown flow cell"
    assert get_tech_type("ABCDEFLT3", FCIDs)[1] == "10B flow cell"
    assert get_tech_type("ABCDEFLT4", FCIDs)[1] == "25B flow cell"


def test_integration():
    res = subprocess.check_output(
        ["python fcid/run.py ABCDEFLT3"],
        shell=True,
    )
    print(res.decode())
    assert res.decode() == "NovaSeq X,NovaSeq X Plus\n"


def test_integration_detailed():
    res = subprocess.check_output(
        ["python fcid/run.py ABCDEFLT3 --detailed"],
        shell=True,
    )
    print(res.decode())
    assert res.decode() == "ABCDEFLT3\tNovaSeq X,NovaSeq X Plus\t10B flow cell\n"


def test_integration_bymachine():
    res = subprocess.check_output(
        ["python fcid/run.py A12345 --by-machine"],
        shell=True,
    )
    print(res.decode())
    assert res.decode() == "NovaSeq 6000\n"

def test_integration_bymachine_detailed():
    res = subprocess.check_output(
        ["python fcid/run.py A12345 --by-machine --detailed"],
        shell=True,
    )
    print(res.decode())
    assert res.decode() == "NovaSeq 6000\n"


def test_dubious_patterns():
    res = subprocess.check_output(
        ["python fcid/run.py H7AP8ADXX"],
        shell=True,
    )
    print(res.decode())
    assert res.decode().startswith("HiSeq")
