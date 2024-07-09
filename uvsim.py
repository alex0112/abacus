#!/usr/bin/env python3

from src.cpu import CPU
from src.memory import Memory
from src.io_device import IODevice
from src.opcodes import Opcode

class UVSim:
    """
    An abstraction representing the UVSim virtual machine. It represents the current state of the virtual machine and creates its memory, register, and CPU.
    """
    def __init__(self, reader=None, writer=None, out_line=None):
        """
        Initialize and create a UVSim VM
        """
        self.__memory = Memory()
        self.__io  = IODevice(reader, writer)
        self.__cpu = CPU(out_line)

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
        try:
            self.cpu.run(self.mem, self.io_device, preview=True)
        except KeyboardInterrupt:
            print("\nAborting...")
            exit(0)

    def store(self, filename):
        """
        Store the contents of memory to a file
        """
        with open(filename, 'w') as program:
            print(f"Storing program to file... {filename} \n")
            counter = len(self.mem) - 1
            while counter > 0:
                if self.mem.read(counter).raw != '+0000':
                    break
                counter -= 1
            for i in range(counter):
                program.write(self.mem.read(i).raw + '\n')
            program.write(self.mem.read(i+1).raw)
            print("Program stored successfully.")
            