#!/usr/bin/env python3
from src.opcode import Opcode


class Memory:
    """
    An abstraction representing the Memory of the UVSim virtual manchine
    """

    def __init__(self, size = 100):
        """
        Create a new memory array for a UVSim virtual machine.
        """
        self.__mem = [Opcode("+0000")] * size

        
    def __len__(self):
        return len(self.__mem)


    def _validate_address(self, address, error_message):
        if address < 0 or address > 99:
            raise ValueError(f"Memory location \"{address}\" is out of boundaries (0-99). {error_message}")

    def _validate_value(self, value, error_message):
        if not isinstance(value, Opcode):
            raise TypeError(f"Expected an Opcode, got \"{type(value)}\" as valued entered. {error_message}")

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
        error_message = "Error while writing."
        self._validate_value(value, error_message)
        self._validate_address(address, error_message)
        if len(self) == 0 & address == 0:
            self.__mem.append(value)
        self.__mem[address] = value
    
    
    def read(self, address):
        error_message = "Error while reading."
        self._validate_address(address, error_message)
        print(self.__mem[address])
        return self.__mem[address]
        
    @property
    def __next(self):
        """
        Return the index of the next unallocated piece of memory

        e.g. ['+1000', '-1000', '+1234'] has a next available address at index 3
        """
        self._validate_address(len(self), "Memory full.")
        return len(self)
    
    def writenext(self, value):
        #self.write(value, self.__next)
        self._validate_value(value, "Error while writing next.")
        self._validate_address(self.__next, "Error while writing next.")
        self.__mem[self.__next] = value
