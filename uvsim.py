#!/usr/bin/env python3

from src.cpu import CPU
from src.memory import Memory
from src.io_device import IODevice
from src.opcode import Opcode

class UVSim:
    """
    An abstraction representing the UVSim virtual machine. It represents the current state of the virtual machine and creates its memory, register, and CPU.
    """
    def __init__(self):
        """
        Initialize and create a UVSim VM
        """
        self.__memory = Memory()
        self.__io  = IODevice()
        self.__cpu = CPU()

    @property
    def mem(self):
        return self.__memory

    @property
    def cpu(self):
        return self.__cpu

    @property
    def io_device(self):
        return self.__io

    def load(self, filename):
        """
        Given a filename load its contents into memory starting at location `00`
        """
        with open(filename) as program:
            #if len(program) > 100: ## TODO: write a check here for memory bounds
            #    pass ## TODO: We need to define behavior for when a program exceeds the available memory

            for line in program:
                opcode = Opcode(line)
                self.mem.writenext(opcode)

    def execute(self):
        """
        Walk through the contents of memory and hand each instruction to the CPU
        """
        #if len(self.mem) == 0:
        #pass ## TODO: define this behavior
        #else:
        self.cpu.run(self.mem, self.io_device)
