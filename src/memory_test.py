import pytest
import pytest
import src.memory as memory
from src.opcodes import Opcode

def test_memory_init():
    mem = memory.Memory()
    assert len(mem) == 100

def test_memory_init_custom_size():
    mem = memory.Memory(200)
    assert len(mem) == 200


def test_memory_write():
    mem = memory.Memory()
    opcode = Opcode("+0010")
    mem.write(opcode, 0)
    assert mem.read(0) == opcode


def test_memory_write_multiple():
    mem = memory.Memory()
    opcode1 = Opcode("+0010")
    opcode2 = Opcode("+0020")
    opcode3 = Opcode("+0030")

def test_memory_write_next():
    ''' Be able to write an opcode to memory at the next available location'''
    mem = memory.Memory()
    opcode1 = Opcode("+0010")
    opcode2 = Opcode("+0020")
    mem.write(opcode1, 0)
    mem.write(opcode2, mem.__next)
    assert mem.read(1) == opcode2 # TODO: check on next on the memory class

