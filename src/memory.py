#!/usr/bin/env python3

class Memory:
    """
    An abstraction representing the Memory of the UVSim virtual machine.
    """

    def __init__(self):
        """
        Create a new memory array for a UVSim virtual machine.
        Initializes memory with 100 words, each initialized to 0.
        """
        self.__mem = [0] * 100  # Assuming memory size is 100 words

    @property
    def mem(self):
        """
        Get the memory.
        """
        return self.__mem

    def write(self, address, value):
        """
        Set the value (should be a signed opcode/number) at a specific index.
        
        Args:
            address (int): The memory address to write to.
            value (int): The value to write at the specified address.

        Raises:
            IndexError: If the address is out of bounds.
        """
        if 0 <= address < len(self.__mem):
            self.__mem[address] = value
        else:
            raise IndexError("Memory address out of range")

    def read(self, address):
        """
        Get the value at a specific index.
        
        Args:
            address (int): The memory address to read from.

        Returns:
            int: The value at the specified address.

        Raises:
            IndexError: If the address is out of bounds.
        """
        if 0 <= address < len(self.__mem):
            return self.__mem[address]
        else:
            raise IndexError("Memory address out of range")

    @property
    def __next(self):
        """
        Return the index of the next unallocated piece of memory.
        
        Returns:
            int: The index of the next available address.
        """
        return len(self.mem)

    def writenext(self, value):
        """
        Write the value at the next available address.
        
        Args:
            value (int): The value to write at the next available address.
        """
        self.write(self.__next, value)