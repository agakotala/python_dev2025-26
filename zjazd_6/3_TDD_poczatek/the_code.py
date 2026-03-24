from functions import multiply
import math

def test_basic():
    assert multiply(1, 2) == 2
    assert multiply(3, 7) == 21
    assert multiply(3, -3) == -9
    assert multiply(0, 7) == 0
    assert multiply(10, 10) == 100

def test_ulamki():
    assert multiply(1, 1.1) == 1.1
    assert multiply(10, 1.1) == 11
    assert multiply(100, 1.1) == 110
    # assert multiply(0.1, 0.000001) == 0.0000001
    assert multiply(math.sqrt(7), math.sqrt(7)) == 7






