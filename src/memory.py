#!/usr/bin/env python3

class Memory:
    """
    An abstraction representing the Memory of the UVSim virtual manchine
    """

    def __init__(self):
        """
        Create a new memory array for a UVSim virtual machine.
        """
        self.__mem = []

    @property
    def mem(self):
        """
        Get the memory
        """
        return self.__mem

    def write(self, value, address):
        """
        Set the value (should be a signed opcode/number) at a specific index.

        If the memory has not yet been allocated, create it.
        """
        pass ## TODO write me

    @property
    def __next(self):
        """
        Return the index of the next unallocated piece of memory

        e.g. ['+1000', '-1000', '+1234'] has a next available address at index 3
        """
        return len(self.mem)

    def writenext(self, value):
        self.write(value, self.__next)
