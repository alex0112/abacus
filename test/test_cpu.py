import sys
import os
import pytest
from unittest.mock import MagicMock
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
def io_device(mocker):
    return mocker.Mock(spec=IODevice)

# Your friend's tests
def test_memory_init():
    mem = Memory()
    assert len(mem.mem) == 100

def test_memory_write():
    mem = Memory()
    mem.write(0, 10)
    assert mem.read(0) == 10

def test_memory_write_multiple():
    mem = Memory()
    mem.write(0, 10)
    mem.write(1, 20)
    mem.write(2, 30)
    assert mem.read(0) == 10
    assert mem.read(1) == 20
    assert mem.read(2) == 30

def test_memory_write_out_of_bounds():
    mem = Memory()
    with pytest.raises(IndexError):
        mem.write(100, 10)

# Your tests
def test_read_success(cpu, memory, io_device):
    io_device.read.return_value = 1234
    cpu.process(1010, memory, io_device)
    assert memory.read(10) == 1234

def test_read_failure(cpu, memory, io_device):
    with pytest.raises(IndexError):
        cpu.process(10100, memory, io_device)

def test_write_success(cpu, memory, io_device):
    memory.write(20, 5678)
    cpu.process(1120, memory, io_device)
    io_device.write.assert_called_once_with(5678)

def test_write_failure(cpu, memory, io_device):
    with pytest.raises(IndexError):
        cpu.process(11100, memory, io_device)

def test_load_success(cpu, memory):
    memory.write(30, 9101)
    cpu.process(2030, memory, None)
    assert cpu.acc == 9101

def test_load_failure(cpu, memory):
    with pytest.raises(IndexError):
        cpu.process(20200, memory, None)

# Updated Unit Test 
def test_store(cpu, memory):
    cpu = CPU()
    mem = Memory()
    cpu.acc = Opcode("+1234")
    cpu.store(mem, 1)
    assert cpu.acc == mem[1]



def test_store_failure(cpu, memory):
    cpu.acc = 1122
    with pytest.raises(IndexError):
        cpu.process(21100, memory, None)

# Arithmetic tests
def test_add_success(cpu, memory):
    memory.write(40, 1234)
    cpu.acc = 5678
    cpu.process(3040, memory, None)  # ADD 1234 to 5678
    assert cpu.acc == (5678 + 1234) % 10000

def test_add_failure(cpu, memory):
    with pytest.raises(IndexError):
        cpu.process(30100, memory, None)  # ADD from invalid address

def test_subtract_success(cpu, memory):
    memory.write(50, 1234)
    cpu.acc = 5678
    cpu.process(3150, memory, None)  # SUBTRACT 1234 from 5678
    assert cpu.acc == (5678 - 1234) % 10000

def test_subtract_failure(cpu, memory):
    with pytest.raises(IndexError):
        cpu.process(31100, memory, None)  # SUBTRACT from invalid address

def test_multiply_success(cpu, memory):
    memory.write(60, 2)
    cpu.acc = 1234
    cpu.process(3260, memory, None)  # MULTIPLY 1234 by 2
    assert cpu.acc == (1234 * 2) % 10000

def test_multiply_failure(cpu, memory):
    with pytest.raises(IndexError):
        cpu.process(32100, memory, None)  # MULTIPLY from invalid address

def test_divide_success(cpu, memory):
    memory.write(70, 2)
    cpu.acc = 1234
    cpu.process(3370, memory, None)  # DIVIDE 1234 by 2
    assert cpu.acc == (1234 // 2) % 10000

def test_divide_failure(cpu, memory):
    with pytest.raises(IndexError):
        cpu.process(33100, memory, None)  # DIVIDE from invalid address

def test_divide_by_zero(cpu, memory):
    memory.write(80, 0)
    cpu.acc = 1234
    with pytest.raises(ZeroDivisionError):
        cpu.process(3380, memory, None)  # DIVIDE 1234 by 0
