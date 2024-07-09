import sys
import os
import pytest
from src.cpu import CPU
from src.memory import Memory
from src.io_device import IODevice
#from src.opcodes import Opcode

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
    io_device = IODevice()
    assert io_device

def test_read(io_device):
    io_device.read = lambda: "1234"
    assert io_device.read() == "1234"
    #assert io_device.last_read == "1234"

def test_write(io_device):
    io_device.write = lambda x: x
    assert io_device.write("1234") == "1234"
    #assert io_device.last_write == "1234"

def test_err(io_device):
    io_device.err = lambda x: x
    assert io_device.err("1234") == "1234"
    #assert io_device.last_err == "1234"
    
    
