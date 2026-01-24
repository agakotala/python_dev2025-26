from functions import fissbuzz

def tests_basic():
    assert fissbuzz(1) == 1
    assert fissbuzz(2) == 2
    assert fissbuzz(3) == 'fiss'
    assert fissbuzz(5) == 'buzz'
    assert fissbuzz(15) == 'fissbuzz'
    assert fissbuzz(35) == 'buzz'

def test_ujemne():
    assert fissbuzz(-3) == 0

def test_slowa():
    assert fissbuzz('mama') == None

def test_float():
    assert fissbuzz(4.2) == 4
    assert fissbuzz(4.9) == 4
    assert fissbuzz(15.9) == 'fissbuzz'