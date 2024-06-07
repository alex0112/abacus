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
        if address < 0 or address > 99:
            raise ValueError(f"Memory location \"{address}\" is out of boundaries (0-99). {error_message}")

    def _validate_value(self, value, error_message):
        if not isinstance(value, Opcode):
            raise TypeError(f"Expected an Opcode, got \"{type(value)}\" as valued entered. {error_message}")

    @property
    def mem(self):
        """
        Get the memory.
        """
        return self.__mem


    def write(self, value, address):
        """
        Set the value (should be a signed opcode/number) at a specific index.
        
        Args:
            address (int): The memory address to write to.
            value (int): The value to write at the specified address.

        Raises:
            IndexError: If the address is out of bounds.
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
        Return the index of the next unallocated piece of memory.
        
        Returns:
            int: The index of the next available address.
        """
        counter = 0
        for opcode_slot in self.__mem:
            if opcode_slot.__raw == Opcode("+0000").__raw:
                return counter
            counter += 1
        raise ValueError("Memory is full.")
    
    def writenext(self, value):

        self.write(value, self.__next)
        self._validate_value(value, "Error while writing next.")
        self._validate_address(self.__next, "Error while writing next.")
        self.__mem[self.__next] = value

