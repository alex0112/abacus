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
    assert isinstance(mem, Memory)

def test_init_from_list():
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002")])

    assert mem.mem[0] == Opcode("+0000")
    assert mem.mem[1] == Opcode("+0001")
    assert mem.mem[2] == Opcode("+0002")

def test_bad_init_from_list():
    mem = Memory()
    with pytest.raises(IndexError):
        mem.write(1000000000000, 0)

########
# Read #
########
def test_default_read():
    mem = Memory()

    assert mem.read(42) == Opcode("+0000")

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


########################
# Addressing & Slicing #
########################

def test_index():
    pass
    memory = Memory()

    


###########
# Preview #
###########

def test_preview():
    pass
