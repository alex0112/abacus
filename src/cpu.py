#!/usr/bin/env python3

class CPU:
    """
    An abstraction representing a CPU.
    This CPU contains an accumulator register and processes opcodes to perform various operations.
    """
    def __init__(self):
        """
        Initialize the CPU with an accumulator set to 0000.
        The accumulator is used for arithmetic and data manipulation operations.
        """
        self.__acc = 0

    @property
    def acc(self):
        """
        Return the current state of the accumulator register in the VM.
        The accumulator is a central component for performing calculations.
        """
        return self.__acc

    @acc.setter
    def acc(self, val):
        """
        Update the current state of the accumulator register in the VM.
        This allows setting the accumulator to a new value during operations.
        """
        self.__acc = val

    def read(self, memory, io_device, address):
        """
        Read a word from the keyboard into a specific location in memory.
        
        Args:
            memory (Memory): The memory object where data will be written.
            io_device (IODevice): The I/O device used for reading input.
            address (int): The memory address where the input data will be stored.
        """
        data = io_device.read()
        memory.write(address, data)

    def write(self, memory, io_device, address):
        """
        Write a word from a specific location in memory to the screen.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            io_device (IODevice): The I/O device used for writing output.
            address (int): The memory address from which the data will be read.
        """
        data = memory.read(address)
        io_device.write(data)

    def load(self, memory, address):
        """
        Load a word from a specific location in memory into the accumulator.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address from which the data will be loaded into the accumulator.
        """
        self.acc = memory.read(address)

    def store(self, memory, address):
        """
        Store a word from the accumulator into a specific location in memory.
        
        Args:
            memory (Memory): The memory object where data will be written.
            address (int): The memory address where the accumulator data will be stored.
        """
        memory.write(address, self.acc)

    def process(self, opcode, memory, io_device):
        """
        Given an opcode, memory object, and peripherals, modify the memory according to the instruction and value given.
        
        Args:
            opcode (int): The opcode to be processed.
            memory (Memory): The memory object involved in the operation.
            io_device (IODevice): The I/O device involved in the operation.
        
        Raises:
            ValueError: If an unknown opcode is encountered.
            IndexError: If the address is out of bounds.
        """
        if not 1000 <= opcode < 10000:
            raise ValueError(f"Invalid opcode format: {opcode}")

        instruction = opcode // 100
        address = opcode % 100

        print(f"Processing opcode {opcode}, instruction {instruction}, address {address}")

        if not 0 <= address < len(memory.mem):
            raise IndexError(f"Memory address out of range: {address}")

        if instruction == 10:  # READ
            self.read(memory, io_device, address)
        elif instruction == 11:  # WRITE
            self.write(memory, io_device, address)
        elif instruction == 20:  # LOAD
            self.load(memory, address)
        elif instruction == 21:  # STORE
            self.store(memory, address)
        else:
            raise ValueError(f"Unknown opcode: {instruction}")