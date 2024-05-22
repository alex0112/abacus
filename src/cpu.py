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
