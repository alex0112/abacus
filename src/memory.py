# src/memory.py

class Memory:
    """
    Class to represent the memory of the simulator.
    """
    def __init__(self):
        self.__mem = [0] * 100  # Initialize memory with 100 locations set to 0

    def __len__(self):
        """
        Returns the length of the memory.
        """
        return len(self.__mem)

    @property
    def mem(self):
        """
        Returns the memory.
        """
        return self.__mem

    def write(self, address, value):
        """
        Writes a value to a specific memory address.
        
        Args:
            address (int): The memory address to write to.
            value (int): The value to write to the memory address.
        
        Raises:
            IndexError: If the address is out of range.
        """
        if address < 0 or address >= len(self.__mem):
            raise IndexError("Memory address out of range")
        self.__mem[address] = value

    def read(self, address):
        """
        Reads a value from a specific memory address.
        
        Args:
            address (int): The memory address to read from.
        
        Raises:
            IndexError: If the address is out of range.
        """
        if address < 0 or address >= len(self.__mem):
            raise IndexError("Memory address out of range")
        return self.__mem[address]

    @property
    def __next(self):
        """
        Finds the next available memory address.
        """
        for i, value in enumerate(self.__mem):
            if value == 0:
                return i
        return len(self.__mem)

    def writenext(self, value):
        """
        Writes a value to the next available memory address.
        
        Args:
            value (int): The value to write to the memory.
        
        Raises:
            IndexError: If there are no available memory addresses.
        """
        next_addr = self.__next
        if next_addr >= len(self.__mem):
            raise IndexError("No available memory address")
        self.write(next_addr, value)