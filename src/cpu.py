#!/usr/bin/env python3

from .opcode import Opcode

class CPU:
    """
    An abstraction representing a CPU
    """
    def __init__(self):
        """
        Create a new CPU for a UVSim virtual machine.
        """
        self.__acc = Opcode("0000")
        self.__current = 0 ## Where to start executing the program.
        self.__halted = False ## Whether or not the current execution should stop

    @property
    def acc(self):
        """
        Return the current state of the accumulator register in the VM
        """
        return self.__acc

    @acc.setter
    def acc(self, val):
        """
        Update the current state of the accumulator register in the VM
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
        Given an opcode, memory object, and peripherals, modify the memory according to the instruction and value given
        """
        match opcode.name:
            case "READ":
                self.read(memory, opcode.operand, io_device)
            case "WRITE":
                self.write(memory, opcode.operand, io_device)
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

    def read(self, memory, address, iodevice):
        pass

    def write(self, memory, address, iodevice):
        pass

    def load(self, memory, address):
        pass

    def store(self, memory, address):
        pass

    
    def add(self, memory, address):
        self.acc += memory.read(address)

        if self.acc > 9999 and self.acc < -9999:
            self.acc = self.acc % 10000
            raise "The values added were greater than storage capacity.  Maintaining the last four digits."


    def subtract(self, memory, address):
        self.acc -= memory.read(address)

        if self.acc > 9999 and self.acc < -9999:
            self.acc = self.acc % 10000
            raise "The values subtracted were greater than storage capacity.  Maintaining the last four digits."


    def multiply(self, memory, address):
        self.acc *= memory.read(address)

        if self.acc > 9999 and self.acc < -9999:
            self.acc = self.acc % 10000
            raise "The values multiplied were greater than storage capacity.  Maintaining the last four digits."

    def divide(self, memory, address):
        if memory.read(address) != 0:
            self.acc //= memory.read(address)
        else:
            raise "The value stored in memory is 0."
        

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
