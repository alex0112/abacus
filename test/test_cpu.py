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
        cpu.current = 250  # Upper Bound is 249

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
    io_device.read = lambda: "7777"
    op = Opcode("1010")
    cpu.process(op, memory, io_device)
    print(memory.read(10))
    assert memory.read(10) == 7777 

def test_read_bad_word(cpu, memory, io_device):
    with pytest.raises(ValueError):
        op = Opcode("10100")
        io_device.read = lambda: "1234"
        cpu.process(op, memory, io_device)

#########
# WRITE #
#########
def test_write(cpu, memory, io_device):
    memory.write(20, 5678)
    io_device.write = lambda x: str(x)
    op = Opcode("1120")
    cpu.process(op, memory, io_device)
    assert io_device.write(5678) == "5678"

def test_write_bad_word(cpu, memory, io_device):
    with pytest.raises(ValueError):
        op = Opcode("11100000000000")
        cpu.process(op, memory, io_device)

########
# LOAD #
########

def test_load(cpu, memory):
    memory.write(30, Opcode("9101"))
    op = Opcode("2030")
    cpu.process(op, memory, None)
    assert cpu.acc == Opcode("9101")

def test_load_bad_word(cpu, memory):
    with pytest.raises(ValueError):
        op = Opcode("20200")
        cpu.process(op, memory, None)

#########
# STORE #
#########
def test_store(cpu, memory, io_device):
    op = Opcode("+1337")
    cpu.acc = op
    cpu.store(memory, 42)
    assert memory.read(42) == int(str(op))

def test_store_bad_word(cpu, memory):
    with pytest.raises(ValueError):
        cpu.acc = Opcode("1234")
        op = Opcode("21200")
        cpu.process(op, memory, None)

#######
# ADD #
#######

def test_add(cpu, memory, io_device):
    cpu.acc = Opcode("001234")
    memory.write(40, Opcode("001000"))
    op = Opcode("030040")
    cpu.process(op, memory, None)
    assert cpu.acc == Opcode("+002234")

def test_add_bad_word(cpu, memory, io_device):
    with pytest.raises(ValueError):
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
    assert cpu.acc == Opcode("+4444")

def test_subtract_bad_word(cpu, memory, io_device):
    with pytest.raises(ValueError):
        op = Opcode("31100")
        cpu.process(op, memory, None)

############
# MULTIPLY #
############

def test_multiply(cpu, memory, io_device):
    op1 = Opcode("+0005")
    op2 = Opcode("+0003")

    cpu.acc = op1 ## 5
    memory.write(42, op2) ## 3

    cpu.multiply(memory, 42)

    assert cpu.acc == Opcode("+0015")

def test_multiply_bad_word(cpu, memory, io_device):
    with pytest.raises(ValueError):
        op = Opcode("32100")
        cpu.process(op, memory, None)

##########
# DIVIDE #
##########

def test_divide(cpu, memory, io_device):
    op1 = Opcode("+0004")
    op2 = Opcode("+0002")

    cpu.acc = op1
    memory.write(42, op2)

    cpu.divide(memory, 42)

    assert cpu.acc == Opcode("+0002")

def test_divide_rem(cpu, memory, io_device):
    op1 = Opcode("+0005")
    op2 = Opcode("+0002")

    cpu.acc = op1
    memory.write(42, op2)

    cpu.divide(memory, 42)

    assert cpu.acc == Opcode("+0002")

def test_divide_bad_word(cpu, memory, io_device):
    with pytest.raises(ValueError):
        op = Opcode("33100")
        cpu.process(op, memory, None)

def test_divide_by_zero(cpu, memory, io_device):
    op1 = Opcode("+0009")
    op2 = Opcode("+0000")

    cpu.acc = op1
    memory.write(42, op2)

    with pytest.raises(ZeroDivisionError):
        cpu.divide(memory, 42)

##########
# BRANCH #
##########

def test_branch(cpu, memory, io_device):
    cpu.acc = Opcode("1234")
    op = Opcode("4040")
    cpu.process(op, memory, io_device)
    assert cpu.current == 40
