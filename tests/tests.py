import sys
sys.path.append('./src') # must be before `from Compressor import Compressor`
from Compressor import Compressor
from utils import read_file

# To run the tests, run the following command in the terminal:
# pytest -v tests/tests.py

path = "./tests/alice.txt"
compressor = Compressor(path)
compressor.compress()

def test_freq_file():
    ref_alice_ref = read_file("./tests/reference_alice_freq.txt")
    alice_ref = read_file("./tests/alice_freq.txt")
    assert ref_alice_ref == alice_ref

def test_comp_file():
    ref_alice_ref = read_file("./tests/reference_alice_comp.bin", "b")
    alice_ref = read_file("./tests/alice_comp.bin", "b")
    assert ref_alice_ref == alice_ref
    
