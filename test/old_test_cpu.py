import sys
import os
import pytest
from unittest.mock import MagicMock

# Ensure the src directory is in the Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from cpu import CPU
from memory import Memory
from io_device import IODevice
from opcodes import Opcode

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
        cpu.current = 100 ## Upper Bound is 99

def test_underflow(cpu):
    with pytest.raises(IndexError):
        cpu.current = -1 ## Lower Bound is 0

############
# Halting: #
############

def test_halt_from_index(cpu):
    ## CPU should not start in a halted state
    assert not cpu.halted
    
    cpu.current = 99
    assert cpu.halted

def test_halt_from_instruction(cpu, memory, io_device):
    op = Opcode("4300") ## HALT

    cpu.process(op, memory, io_device)

    assert cpu.halted
    
########
# READ #
########

def test_read_good_word(cpu, memory, io_device):
    io_device.read = MagicMock(return_value="1234")
    op = Opcode("1010")  # READ into address 10

    cpu.process(op, memory, io_device)

    assert memory.read(10) == "1234"

def test_read_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("10100")  # READ into invalid address 100
        io_device.read = MagicMock(return_value="1234")
        cpu.process(op, memory, io_device)

#########
# WRITE #
#########

def test_write(cpu, memory, io_device):
    memory.write(20, "5678")
    io_device.write = MagicMock()
    op = Opcode("1120")  # WRITE from address 20

    cpu.process(op, memory, io_device)

    io_device.write.assert_called_once_with("5678")

def test_write_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("11100")  # WRITE from invalid address 100
        cpu.process(op, memory, io_device)

########
# LOAD #
########

def test_load(cpu, memory):
    memory.write(30, "9101")
    op = Opcode("2030")  # LOAD from address 30

    cpu.process(op, memory, None)

    assert cpu.acc == "9101"

def test_load_bad_word(cpu, memory):
    with pytest.raises(IndexError):
        op = Opcode("20200")  # LOAD from invalid address 200
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
        cpu.acc = "1234"
        op = Opcode("21200")  # STORE into invalid address 200
        cpu.process(op, memory, None)

#######
# ADD #
#######

def test_add(cpu, memory, io_device):
    cpu.acc = "1234"
    memory.write(40, "1000")
    op = Opcode("3040")  # ADD from address 40

    cpu.process(op, memory, None)

    assert cpu.acc == "2234"

def test_add_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("30100")  # ADD from invalid address 100
        cpu.process(op, memory, None)

############
# SUBTRACT #
############

def test_subtract(cpu, memory, io_device):
    cpu.acc = "5678"
    memory.write(50, "1234")
    op = Opcode("3150")  # SUBTRACT from address 50

    cpu.process(op, memory, None)

    assert cpu.acc == "4444"

def test_subtract_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("31100")  # SUBTRACT from invalid address 100
        cpu.process(op, memory, None)

############
# MULTIPLY #
############

def test_multiply(cpu, memory, io_device):
    cpu.acc = "1234"
    memory.write(60, "2")
    op = Opcode("3260")  # MULTIPLY from address 60

    cpu.process(op, memory, None)

    assert cpu.acc == "2468"

def test_multiply_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("32100")  # MULTIPLY from invalid address 100
        cpu.process(op, memory, None)

##########
# DIVIDE #
##########

def test_divide(cpu, memory, io_device):
    cpu.acc = "1234"
    memory.write(70, "2")
    op = Opcode("3370")  # DIVIDE from address 70

    cpu.process(op, memory, None)

    assert cpu.acc == "0617"

def test_divide_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("33100")  # DIVIDE from invalid address 100
        cpu.process(op, memory, None)

def test_divide_by_zero(cpu, memory, io_device):
    cpu.acc = "1234"
    memory.write(80, "0")
    with pytest.raises(ZeroDivisionError):
        op = Opcode("3380")  # DIVIDE by 0
        cpu.process(op, memory, None)

##########
# BRANCH #
##########

def test_branch(cpu, memory, io_device):
    cpu.acc = "1234"
    op = Opcode("4040")  # BRANCH to address 40

    cpu.process(op, memory, io_device)

    assert cpu.current == 40

def test_branch_bad_word(cpu, memory, io_device):
    with pytest.raises(IndexError):
        op = Opcode("40100")  # BRANCH to invalid address 100
        cpu.process(op, memory, io_device)

#############
# BRANCHNEG #
#############

def test_branchneg(cpu, memory, io_device):
    cpu.acc = "-1234"
    op = Opcode("4140")  # BRANCHNEG to address 40

    cpu.process(op, memory, io_device)

    assert cpu.current == 40

def test_branchneg_positive(cpu, memory, io_device):
    cpu.acc = "1234"
    op = Opcode("4140")  # BRANCHNEG to address 40

    cpu.process(op, memory, io_device)

    assert cpu.current != 40

##############
# BRANCHZERO #
##############

def test_branchzero(cpu, memory):
    cpu.acc = "0000"
    op = Opcode("4240")  # BRANCHZERO to address 40

    cpu.process(op, memory, None)

    assert cpu.current == 40

def test_branchzero_nonzero(cpu, memory):
    cpu.acc = "1234"
    op = Opcode("4240")  # BRANCHZERO to address 40

    cpu.process(op, memory, None)

    assert cpu.current != 40