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
    mem = Memory([-1234])

    assert mem == [Opcode("-1234")]

def test_bad_init_from_list():
    with pytest.raises(ValueError):
        mem = Memory([1000000000000])

########
# Read #
########
def test_read():
    memory = Memory([1234, 4567, 8910])

    assert memory.read(0) == Opcode("+1234")

#########
# Write #
#########
def test_write(memory):
    memory.write(12, 1234)

    assert memory.read(12) == Opcode("+1234")


########################
# Write Next Available #
########################
def test_writenext():
    memory = Memory([1234, 5678, 8910])
    op = Opcode("+1112")

    memory.writenext(op)

    assert memory.read(3) == op

## TODO: Write more tests

    
