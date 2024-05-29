#!/usr/bin/env python3

import CPU
import Memory
import IODevice

class UVSim:
    """
    An abstraction representing the UVSim virtual machine. It represents the current state of the virtual machine and creates its memory, register, and CPU.
    """
    def __init__():
        """
        Initialize and create a UVSim VM
        """
        self.__memory = Memory.new()
        self.__io  = IODevice.new()
        self.__cpu = CPU.new()

    @property
    def mem(self):
        return self.__memory

    @property
    def cpu(self):
        return self.__cpu

    @property
    def io_device:
        return self.__io

    def load(self, filename):
        """
        Given a filename load its contents into memory starting at location `00`
        """
        with open(filename) as program:
            if len(program) > 100:
                pass ## TODO: We need to define behavior for when a program exceeds the available memory

            for opcode in program:
                self.mem.writenext(opcode)

    def execute(self):
        """
        Walk through the contents of memory and hand each instruction to the CPU
        """
        if len(self.mem) == 0:
            pass ## TODO: define this behavior
        else:
            for raw_num in self.mem:
                opcode = Opcode.new(raw_num) ## see opcode.py

                self.cpu.process(opcode, self.mem, self.io_device)

        
