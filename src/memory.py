#!/usr/bin/env python3
from src.opcodes import Opcode

class Memory:
    """
    An abstraction representing the Memory of the UVSim virtual machine.
    """

    def __init__(self, size = 100):
        """
        Create a new memory array for a UVSim virtual machine.
        Initializes memory with 100 words, each initialized to 0.
        """

        self.__mem = [Opcode("+0000")] * size

        
    def __len__(self):
        return len(self.__mem)


    def _validate_address(self, address, error_message):
        '''Validate the address to ensure it is within the boundaries of the memory array.'''
        if address < 0 or address > 99:
            raise IndexError(f"Memory location \"{address}\" is out of boundaries (0-99). {error_message}")

    def _validate_value(self, value, error_message):
        '''Validate the value to ensure it is an instance of Opcode.'''
        if not isinstance(value, Opcode):
            raise TypeError(f"Expected an Opcode, got \"{type(value)}\" as valued entered. {error_message}")

    @property
    def mem(self):
        """
        Get the memory.
        """
        return self.__mem



    def write(self, address, value):

        """
        Set the value (should be a signed opcode) at a specific index.
        Args:
            value (Opcode): The opcode to write at the specified address.
            address (int): The memory address to write to."""
        error_message = "Error while writing."
        self._validate_value(value, error_message)
        self._validate_address(address, error_message)
        if len(self) == 0 & address == 0:
            self.__mem.append(value)
        self.__mem[address] = value
    
    
    def read(self, address):
        '''Read the value at the specified address. Raises error if invalid address is provided.'''
        error_message = "Error while reading."
        self._validate_address(address, error_message)
        return int(str(self.__mem[address]))
        
    @property
    def next(self):
        """
        Return the index of the next unallocated piece of memory.

        Returns:
            int: The index of the next available address.
        """
        #this is the method that is not recognized on the pytest
        counter = 0
        for opcode_slot in self.__mem:
            if str(opcode_slot) == Opcode("+0000").__str__():
                return counter
            counter += 1
        raise ValueError("Memory is full.")
    def writenext(self, value):
        '''calls the next property to input in the write method.'''
        self.write(self.next, value)
        self.__mem[self.next] = value


