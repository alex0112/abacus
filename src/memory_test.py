import pytest
import pytest
import src.memory as memory
from src.opcode import Opcode

def test_memory_init():
    mem = memory.Memory()
    assert len(mem) == 100


def test_memory_write():
    mem = memory.Memory()
    opcode = Opcode(10)
    mem.write(opcode, 0)
    assert mem.read(0) == opcode


def test_memory_write_multiple():
    mem = memory.Memory()
    opcode1 = Opcode(10)
    opcode2 = Opcode(20)
    opcode3 = Opcode(30)
    mem.write(opcode1, 0)
    mem.write(opcode2, 1)
    mem.write(opcode3, 2)
    assert mem.read(0) == opcode1
    assert mem.read(1) == opcode2
    assert mem.read(2) == opcode3


def test_memory_write_out_of_bounds():
    mem = memory.Memory()
    with pytest.raises(ValueError):
        mem.write(Opcode(10), 100)