import sys
import os
import pytest
from src.cpu import CPU
from src.memory import Memory
from src.io_device import IODevice
from src.opcodes import Opcode

# Ensure the src directory is in the Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def cpu():
    return CPU()

@pytest.fixture
def memory():
    return Memory()

@pytest.fixture
def io_device():
    return IODevice()

##################
# Initialization #
##################
def test_init():
    mem = Memory()
    assert mem

def test_init_from_list():
    mem = Memory()
    mem.write(0, -1234)
    assert mem.read(0) == -1234
a
def test_bad_init_from_list():
    mem = Memory()
    with pytest.raises(IndexError):
        mem.write(1000000000000, 0)

########
# Read #
########
def test_read():
    memory = Memory()
    memory.write(0, 1234)
    memory.write(1, 4567)
    memory.write(2, 8910)
    assert memory.read(0) == 1234
    assert memory.read(1) == 4567
    assert memory.read(2) == 8910

#########
# Write #
#########
def test_write(memory):
    memory.write(12, 1234)
    assert memory.read(12) == 1234

########################
# Write Next Available #
########################
def test_writenext():
    memory = Memory()
    memory.write(0, 1234)
    memory.write(1, 5678)
    memory.write(2, 8910)
    memory.writenext(1112)
    assert memory.read(3) == 1112
    
def test_next():
    memory = Memory()
    memory.write(0, 1234)