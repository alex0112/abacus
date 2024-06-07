#!/usr/bin/env python3

from .opcodes import Opcode

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

        self.__acc = Opcode("0000")
        self.__current = 0  # Where to start executing the program.
        self.__halted = False  # Whether or not the current execution should stop

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
        """
        self.__acc = val

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, val):
        if val > 99 or val < 0:
            raise IndexError(f"Attempted to set current address to {val}. Cannot set to a value that is not between 0-99 inclusive.")
        elif val == 99:
            self.halted = True

        self.__current = val

    @property
    def halted(self):
        return self.__halted

    @halted.setter
    def halted(self, val):
        self.__halted = val

    def run(self, memory, io_device, address=0):
        self.current = address

        while not self.halted:
            if self.current > len(memory) - 1 or len(memory) == 0:  # If we reach the end of the program it's over
                self.halted = True
                break

            current_opcode = memory.read(self.current)
            self.process(current_opcode, memory, io_device)
            self.current += 1  # Move on to the next address

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

        match opcode.name:
            case "READ":
                self.read(memory, io_device, int(opcode.operand))  # Fixed typo and cast operand to int
            case "WRITE":
                self.write(memory, io_device, int(opcode.operand))  # Fixed typo and cast operand to int
            case "LOAD":
                self.load(memory, int(opcode.operand))  # Cast operand to int
            case "STORE":
                self.store(memory, int(opcode.operand))  # Cast operand to int
            case "ADD":
                self.add(memory, int(opcode.operand))  # Fixed typo and cast operand to int
            case "SUBTRACT":
                self.subtract(memory, int(opcode.operand))  # Cast operand to int
            case "MULTIPLY":
                self.multiply(memory, int(opcode.operand))  # Cast operand to int
            case "DIVIDE":
                self.divide(memory, int(opcode.operand))  # Cast operand to int
            case "BRANCH":
                self.branch(memory, int(opcode.operand))  # Cast operand to int
            case "BRANCHNEG":
                self.branchneg(memory, int(opcode.operand))  # Cast operand to int
            case "BRANCHZERO":
                self.branchzero(memory, int(opcode.operand))  # Cast operand to int
            case "HALT":
                self.halt()
            case _:
                self.noop()  # In this case treat the opcode as a raw piece of data and not an instruction

    def read(self, memory, io_device, address):
        """
        Read a word from the keyboard into a specific location in memory.
        
        Args:
            memory (Memory): The memory object where data will be written.
            io_device (IODevice): The I/O device used for reading input.
            address (int): The memory address where the input data will be stored.
        """
        data = int(io_device.read())  # Ensure data is integer
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
        memory.write(address, int(str(self.acc)))  # Ensure acc is written as integer

    def add(self, memory, address):
        """
        Add a word from a specific location in memory to the accumulator.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address from which the data will be added to the accumulator.
        """
        self.acc = Opcode(f"{int(str(self.acc)) + memory.read(address):+05d}")

    def subtract(self, memory, address):
        """
        Subtract a word from a specific location in memory from the accumulator.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address from which the data will be subtracted from the accumulator.
        """
        self.acc = Opcode(f"{int(str(self.acc)) - memory.read(address):+05d}")

    def multiply(self, memory, address):
        """
        Multiply a word from a specific location in memory with the accumulator.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address from which the data will be multiplied with the accumulator.
        """
        self.acc = Opcode(f"{int(str(self.acc)) * memory.read(address):+05d}")

    def divide(self, memory, address):
        """
        Divide the accumulator by a word from a specific location in memory.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address from which the data will be used to divide the accumulator.
        """
        divisor = memory.read(address)
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.acc = Opcode(f"{int(str(self.acc)) // divisor:+05d}")

    def branch(self, memory, address):
        """
        Branch to a specific location in memory.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address to branch to.
        """
        self.current = address

    def branchneg(self, memory, address):
        """
        Branch to a specific location in memory if the accumulator is negative.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address to branch to.
        """
        if int(str(self.acc)) < 0:
            self.current = address

    def branchzero(self, memory, address):
        """
        Branch to a specific location in memory if the accumulator is zero.
        
        Args:
            memory (Memory): The memory object where data will be read from.
            address (int): The memory address to branch to.
        """
        if int(str(self.acc)) == 0:
            self.current = address

    def halt(self):
        self.halted = True

    def noop(self):
        pass