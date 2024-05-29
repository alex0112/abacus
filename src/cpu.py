#!/usr/bin/env python3

class CPU:
    """
    An abstraction representing a CPU
    """
    def __init__():
        """
        Create a new CPU for a UVSim virtual machine.
        """
        self.__acc = 0000

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


    def process(self, opcode, memory, io_device):
        """
        Given an opcode, memory object, and peripherals, modify the memory according to the instruction and value given
        """
        ## TODO: This is where we'll need to farm out the different operands and functions
        pass
