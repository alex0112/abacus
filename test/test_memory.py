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
    mem.write(0, Opcode("-1234"))
    assert mem.read(0) == -1234

def test_bad_init_from_list():
    mem = Memory()
    with pytest.raises(IndexError):
        mem.write(200, Opcode("+0001"))

########
# Read #
########
def test_read():
    memory = Memory()
    memory.write(0, Opcode("+1234"))
    memory.write(1, Opcode("+4567"))
    memory.write(2, Opcode("+8910"))
    assert memory.read(0) == 1234
    assert memory.read(1) == 4567
    assert memory.read(2) == 8910

#########
# Write #
#########
def test_write(memory):
    memory.write(12, Opcode("+8910"))
    assert memory.read(12) == 8910

########################
# Write Next Available #
########################
def test_writenext():
    memory = Memory()
    memory.write(0, Opcode("+1111"))
    memory.write(1, Opcode("+2222"))
    memory.write(2, Opcode("+3333"))
    memory.writenext(Opcode("+4444"))
    assert memory.read(3) == 4444
    