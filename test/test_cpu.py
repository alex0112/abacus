import sys
import os
import pytest
from unittest.mock import MagicMock
from cpu import CPU
from memory import Memory
from io_device import IODevice

# Ensure the src directory is in the Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

@pytest.fixture
def cpu():
    """
    Fixture for initializing the CPU object.
    This fixture ensures that a new instance of the CPU class is available for each test.
    Returns:
        CPU: An instance of the CPU class.
    """
    return CPU()

@pytest.fixture
def memory():
    """
    Fixture for initializing the Memory object.
    This fixture ensures that a new instance of the Memory class is available for each test.
    Returns:
        Memory: An instance of the Memory class.
    """
    return Memory()

@pytest.fixture
def io_device(mocker):
    """
    Fixture for initializing a mocked IODevice object.
    The mocker is used to create mock methods for IO operations.
    Args:
        mocker: The pytest-mock plugin fixture.
    Returns:
        Mock: A mocked instance of the IODevice class.
    """
    return mocker.Mock(spec=IODevice)

def test_read_success(cpu, memory, io_device):
    """
    Test the READ opcode.
    Ensures that data read from the IO device is correctly written to memory.
    """
    # Mock the io_device.read method to return a known value.
    io_device.read.return_value = 1234

    # Execute the READ opcode (1010 means READ to address 10).
    cpu.process(1010, memory, io_device)

    # Check if the value was correctly written to memory.
    assert memory.read(10) == 1234

def test_read_failure(cpu, memory, io_device):
    """
    Test the READ opcode failure condition.
    Ensures that an IOError is raised when the IO device fails to read.
    """
    # Mock the io_device.read method to raise an IOError.
    io_device.read.side_effect = IOError("Failed to read")

    # Execute the READ opcode and expect an IOError.
    with pytest.raises(IOError):
        cpu.process(1010, memory, io_device)

def test_write_success(cpu, memory, io_device):
    """
    Test the WRITE opcode.
    Ensures that data from memory is correctly written to the IO device.
    """
    # Set a known value in memory.
    memory.write(20, 5678)

    # Execute the WRITE opcode (1120 means WRITE from address 20).
    cpu.process(1120, memory, io_device)

    # Check if the value was correctly written to the console.
    io_device.write.assert_called_once_with(5678)

def test_write_failure(cpu, memory, io_device):
    """
    Test the WRITE opcode failure condition.
    Ensures that an IOError is raised when the IO device fails to write.
    """
    # Set a known value in memory.
    memory.write(20, 5678)

    # Mock the io_device.write method to raise an IOError.
    io_device.write.side_effect = IOError("Failed to write")

    # Execute the WRITE opcode and expect an IOError.
    with pytest.raises(IOError):
        cpu.process(1120, memory, io_device)

def test_load_success(cpu, memory):
    """
    Test the LOAD opcode.
    Ensures that data from memory is correctly loaded into the accumulator.
    """
    # Set a known value in memory.
    memory.write(30, 9101)

    # Execute the LOAD opcode (2030 means LOAD from address 30).
    cpu.process(2030, memory, None)

    # Check if the accumulator has the correct value.
    assert cpu.acc == 9101

def test_load_failure(cpu, memory):
    """
    Test the LOAD opcode failure condition.
    Ensures that an IndexError is raised when loading from an invalid memory address.
    """
    # Execute the LOAD opcode with an invalid address (20200 means LOAD from address 200).
    with pytest.raises(IndexError):
        cpu.process(20200, memory, None)

def test_store_success(cpu, memory):
    """
    Test the STORE opcode.
    Ensures that data from the accumulator is correctly stored in memory.
    """
    # Set a known value in the accumulator.
    cpu.acc = 1122

    # Execute the STORE opcode (2130 means STORE to address 30).
    cpu.process(2130, memory, None)

    # Check if the value was correctly written to memory.
    assert memory.read(30) == 1122

def test_store_failure(cpu, memory):
    """
    Test the STORE opcode failure condition.
    Ensures that an IndexError is raised when storing to an invalid memory address.
    """
    # Set a known value in the accumulator.
    cpu.acc = 1122

    # Execute the STORE opcode with an invalid address (21100 means STORE to address 100).
    with pytest.raises(IndexError):
        cpu.process(21100, memory, None)