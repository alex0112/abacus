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

def test_init_from_exact_list():
    size = Memory.LAST_ADDRESS
    arr  = [Opcode("+0000")] * size

    memory = Memory(arr)
    assert isinstance(memory, Memory)

def test_bad_init_from_list():
    mem = Memory()
    with pytest.raises(IndexError):
        mem.write(1000000000000, 0)

def test_bad_init_from_large_list():
    with pytest.raises(IndexError):
        too_big = [Opcode("+0000")] * (Memory.LAST_ADDRESS + 1)

        Memory(too_big)

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
def test_writenext_empty():
    memory = Memory()
    memory.writenext(1042)

    assert memory[0] == Opcode("+1042")

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
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002")])

    assert mem[0] == Opcode("+0000")
    assert mem[1] == Opcode("+0001")
    assert mem[2] == Opcode("+0002")
            

## TODO: This might not actually be desirable behavior so we should make a design decision here
# def test_negative_index():
#     mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002")])

#     assert mem[-1] == ?

def test_slice():
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002"), Opcode("+0003"), Opcode("+0004")])

    assert mem[1:3] == [Opcode("+0001"), Opcode("+0002")]

###########
# Preview #
###########

def test_preview_full():
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002"), Opcode("+0003"), Opcode("+0004")])

    assert mem.preview(2, 5) == { 0: Opcode("+0000"), 1: Opcode("+0001"), 2: Opcode("+0002"), 3: Opcode("+0003"), 4: Opcode("+0004")}

def test_preview_empty():
    mem = Memory()

    assert mem.preview(2, 5) == {0: Opcode("+0000"), 1: Opcode("+0000"), 2: Opcode("+0000"), 3: Opcode("+0000"), 4: Opcode("+0000")} 

def test_preview_begin_odd():
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002"), Opcode("+0003"), Opcode("+0004")])

    assert mem.preview(0, 5) == {0: Opcode("+0000"), 1: Opcode("+0001"), 2: Opcode("+0002"), 3: Opcode("+0003"), 4: Opcode("+0004")}

def test_preview_near_begin_odd():
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002"), Opcode("+0003"), Opcode("+0004")])

    assert mem.preview(1, 5) == {0: Opcode("+0000"), 1: Opcode("+0001"), 2: Opcode("+0002"), 3: Opcode("+0003"), 4: Opcode("+0004")}

def test_preview_begin_even():
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002"), Opcode("+0003"), Opcode("+0004")])

    assert mem.preview(0, 4) == {0: Opcode("+0000"), 1: Opcode("+0001"), 2: Opcode("+0002"), 3: Opcode("+0003"), 4: Opcode("+0004")}

def test_preview_near_begin_even():
    mem = Memory([Opcode("+0000"), Opcode("+0001"), Opcode("+0002"), Opcode("+0003"), Opcode("+0004")])

    assert mem.preview(1, 4) == {0: Opcode("+0000"), 1: Opcode("+0001"), 2: Opcode("+0002"), 3: Opcode("+0003"), 4: Opcode("+0004")}

def test_preview_end_odd():
    mem = Memory()

    mem.write(95, Opcode("+0095"))
    mem.write(96, Opcode("+0096"))
    mem.write(97, Opcode("+0097"))
    mem.write(98, Opcode("+0098"))
    mem.write(99, Opcode("+0099"))

    assert mem.preview(97, 5) == {95: Opcode("+0095"), 96: Opcode("+0096"), 97: Opcode("+0097"), 98: Opcode("+0098"), 99: Opcode("+0099")}

def test_preview_near_end_odd():
    mem = Memory()

    mem.write(95, Opcode("+0095"))
    mem.write(96, Opcode("+0096"))
    mem.write(97, Opcode("+0097"))
    mem.write(98, Opcode("+0098"))
    mem.write(99, Opcode("+0099"))

    assert mem.preview(98, 5) == {95: Opcode("+0095"), 96: Opcode("+0096"), 97: Opcode("+0097"), 98: Opcode("+0098"), 99: Opcode("+0099")}

def test_preview_near_end_even():
    mem = Memory()

    mem.write(95, Opcode("+0095"))
    mem.write(96, Opcode("+0096"))
    mem.write(97, Opcode("+0097"))
    mem.write(98, Opcode("+0098"))
    mem.write(99, Opcode("+0099"))

    assert mem.preview(98, 4) == {95: Opcode("+0095"), 96: Opcode("+0096"), 97: Opcode("+0097"), 98: Opcode("+0098"), 99: Opcode("+0099")}

def test_preview_end_even():
    mem = Memory()

    mem.write(95, Opcode("+0095"))
    mem.write(96, Opcode("+0096"))
    mem.write(97, Opcode("+0097"))
    mem.write(98, Opcode("+0098"))
    mem.write(99, Opcode("+0099"))

    assert mem.preview(99, 4) == {95: Opcode("+0095"), 96: Opcode("+0096"), 97: Opcode("+0097"), 98: Opcode("+0098"), 99: Opcode("+0099")}

def test_memory_iteration():
    mem = Memory()


    mem.write(0, Opcode("+0000"))
    mem.write(1, Opcode("+0001"))

    mem.write(95, Opcode("+0095"))
    mem.write(96, Opcode("+0096"))
    mem.write(97, Opcode("+0097"))
    mem.write(98, Opcode("+0098"))
    mem.write(99, Opcode("+0099"))


    result = []

    for opcode in mem:
        result.append(opcode)

    assert len(result) == 100
    assert result[0] == Opcode("+0000")
    assert result[1] == Opcode("+0001")

    assert result[42] == Opcode("+0000")

    assert result[98] == Opcode("+0098")
    assert result[99] == Opcode("+0099")
    
