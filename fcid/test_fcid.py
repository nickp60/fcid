from run import main, get_tech_type, FCIDs

def test_by_machine(capsys):
    main(query="K12345", by_machine=True)
    outerr = capsys.readouterr()
    assert outerr.out  == "HiSeq 3000,HiSeq 4000\n"

def test_by_flowcell():
    assert get_tech_type("22C37GLT3", FCIDs)[0] == ["NovaSeq X"]
