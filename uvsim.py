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
        self.mem.clear()
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

        # Find the index of the last non-empty opcode
        last_non_empty_index = -1
        for i in range(len(self.mem) - 1, -1, -1):
            if str(self.mem[i]) != '+0000':
                last_non_empty_index = i
                break

        # Write opcodes to the file, including intermediate empty ones
        with open(filename, 'w') as program:
            for i, opcode in enumerate(self.mem):
                if i <= last_non_empty_index:
                    program.write(str(opcode) + "\n")


            
            print('Program saved successfully')
            
    def convert(self, filename):
        """
        Convert the contents of memory to a binary file
        """
        op_list = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
        new_list = []
        with open(filename, 'r') as file:
            #separate each line to be analized
            for line in file:
                if line[0] == "+" or line[0] == "-":
                    current = line[1:]
                if int(current[:2]) in op_list:
                    current = f"{line[0]}0{current[0:2]}0{current[2:]}" #add a 0 to the opcode and 0 to the address
                else:
                    current = f"{line[0]}00{current}" #add 00 to the address if is just valie
                new_list.append(current)
            #print in readable format
            for i in new_list:
                print(i)
                    

        


