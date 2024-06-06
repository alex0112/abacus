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
        self.__current = 0 ## Where to start executing the program.
        self.__halted = False ## Whether or not the current execution should stop

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

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, val):
        if val > 99 or val < 0:
            raise ValueError(f"Attempted to set current address to {val}. Cannot set to a value that is not between 0-99 inclusive.")
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
            if self.current > len(memory)-1 or len(memory) == 0: ## If we reach the end of the program it's over
                self.halted = True
                break

            current_opcode = memory.read(self.current)
            self.process(current_opcode, memory, io_device)
            self.current += 1 ## Move on to the next address


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
                self.read(memory, opcode.operand, iodevice)
            case "WRITE":
                self.write(memory, opcode.operand, iodevice)
            case "LOAD":
                self.load(memory, opcode.operand)
            case "STORE":
                self.store(memory, opcode.operand)
            case "ADD":
                self.store(memory, opcode.operand)
            case "SUBTRACT":
                self.subtract(memory, opcode.operand)
            case "MULTIPLY":
                self.multiply(memory, opcode.operand)
            case "DIVIDE":
                self.divide(memory, opcode.operand)
            case "BRANCH":
                self.branch(memory, opcode.operand)
            case "BRANCHNEG":
                self.branchneg(memory, opcode.operand)
            case "BRANCHZERO":
                self.branchzero(memory, opcode.operand)
            case "HALT":
                self.halt()
            case _:
                self.noop() ## In this case treat the opcode as a raw piece of data and not an instruction

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

    def add(self, memory, address):
        pass

    def subtract(self, memory, address):
        pass

    def multiply(self, memory, address):
        pass

    def divide(self, memory, address):
        pass

    def branch(self, memory, address):
        pass

    def branchneg(self, memory, address):
        pass

    def branchzero(self, memory, address):
        pass

    def halt(self):
        self.halted = True

    def noop(self):
        pass
