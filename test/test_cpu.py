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

###################
# Initialization: #
###################
def test_init():
    cpu = CPU()
    assert not cpu.halted
    assert cpu.current == 0
    assert cpu.acc == Opcode("0000")

####################
# Current Counter: #
####################
def test_overflow(cpu):
    with pytest.raises(IndexError):
        cpu.current = 100  # Upper Bound is 99

def test_underflow(cpu):
    with pytest.raises(IndexError):
        cpu.current = -1  # Lower Bound is 0

############
# Halting: #
############

def test_halt_from_index(cpu):
    assert not cpu.halted
    cpu.current = 99
    assert cpu.halted

def test_halt_from_instruction(cpu, memory, io_device):
    op = Opcode("4300")
    cpu.process(op, memory, io_device)
    assert cpu.halted

########
# READ #
########

def test_read_good_word(cpu, memory, io_device):
    io_device.read = lambda: "1234"
    op = Opcode("1010")
    cpu.process(op, memory, io_device)
    assert memory.read(10) == "1234"

def test_read_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("10100")
        io_device.read = lambda: "1234"
        cpu.process(op, memory, io_device)

#########
# WRITE #
#########

def test_write(cpu, memory, io_device):
    memory.write(20, 5678)
    io_device.write = lambda x: x
    op = Opcode("1120")
    cpu.process(op, memory, io_device)
    assert io_device.write(5678) == "5678"

def test_write_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("11100")
        cpu.process(op, memory, io_device)

########
# LOAD #
########

def test_load(cpu, memory):
    memory.write(30, 9101)
    op = Opcode("2030")
    cpu.process(op, memory, None)
    assert cpu.acc == Opcode("9101")

def test_load_bad_word(cpu, memory):
    with pytest.raises(IndexError):
        op = Opcode("20200")
        cpu.process(op, memory, None)

#########
# STORE #
#########
def test_store(cpu, memory, io_device):
    op = Opcode("+1337")
    cpu.acc = op
    cpu.store(memory, 42)
    assert memory.read(42) == op

def test_store_bad_word(cpu, memory):
    with pytest.raises(IndexError):
        cpu.acc = Opcode("1234")
        op = Opcode("21200")
        cpu.process(op, memory, None)

#######
# ADD #
#######

def test_add(cpu, memory, io_device):
    cpu.acc = Opcode("1234")
    memory.write(40, Opcode("1000"))
    op = Opcode("3040")
    cpu.process(op, memory, None)
    assert cpu.acc == Opcode("2234")

def test_add_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("30100")
        cpu.process(op, memory, None)

############
# SUBTRACT #
############

def test_subtract(cpu, memory, io_device):
    cpu.acc = Opcode("5678")
    memory.write(50, Opcode("1234"))
    op = Opcode("3150")
    cpu.process(op, memory, None)
    assert cpu.acc == Opcode("4444")

def test_subtract_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("31100")
        cpu.process(op, memory, None)

############
# MULTIPLY #
############

def test_multiply(cpu, memory, io_device):
    cpu.acc = Opcode("1234")
    memory.write(60, Opcode("0002"))
    op = Opcode("3260")
    cpu.process(op, memory, None)
    assert cpu.acc == Opcode("2468")

def test_multiply_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("32100")
        cpu.process(op, memory, None)

##########
# DIVIDE #
##########

def test_divide(cpu, memory, io_device):
    cpu.acc = Opcode("1234")
    memory.write(70, Opcode("0002"))
    op = Opcode("3370")
    cpu.process(op, memory, None)
    assert cpu.acc == Opcode("0617")

def test_divide_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("33100")
        cpu.process(op, memory, None)

def test_divide_by_zero(cpu, memory, io_device):
    cpu.acc = Opcode("1234")
    memory.write(80, Opcode("0000"))
    with pytest.raises(ZeroDivisionError):
        op = Opcode("3380")
        cpu.process(op, memory, None)

##########
# BRANCH #
##########

def test_branch(cpu, memory, io_device):
    cpu.acc = Opcode("1234")
    op = Opcode("4040")
    cpu.process(op, memory, io_device)
    assert cpu.current == 40