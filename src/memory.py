from src.opcodes import Opcode

class Memory:
    """
    Class to represent the memory of the simulator.
    """
    ADDRESSABLE_SPACE = range(0, 250)
    LAST_ADDRESS      = ADDRESSABLE_SPACE.stop - 1

    def __init__(self, arr=[]):
        if len(arr) == 0:
            self.__mem = dict()
        elif len(arr) not in Memory.ADDRESSABLE_SPACE:
            raise IndexError(f"Attempted to create a Memory object out of an array of length {len(arr)}. Cannot create object with an array whose length exceeds {Memory.ADDRESSABLE_SPACE.stop}")
        else:
            mem = dict()
            for i in range(len(arr)):
                mem[i] = arr[i]
            self.__mem = mem
        
    def __len__(self):
        """
        Returns the current number of memory locations that have been written to
        """
        return len(self.__mem.keys())

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
        assert isinstance(address, int)

        if address not in Memory.ADDRESSABLE_SPACE:
            raise IndexError("Memory address out of range")

        if isinstance(value, int):
            value = Opcode(value)
        
        self.mem[address] = value

    def read(self, address):
        """
        Reads a value from a specific memory address.
        
        Args:
            address (int): The memory address to read from.
        
        Raises:
            IndexError: If the address is out of range.
        """
        if address not in Memory.ADDRESSABLE_SPACE:
            raise IndexError("Memory address out of range")

        return self.__mem.get(address, Opcode("+0000")) ## Default to +0000 for unwritten memory

    @property
    def __next(self):
        """
        Finds the next available memory address.
        """
        ## Grab all the keys from the memory dictionary
        #  sort them
        #  get the last key
        #  __next value should be that value plus one
        # TODO: Optimize by caching this?
        if len(self.__mem) == 0:
            return 0 ## i.e. if nothing has yet to be written return the start
        else:
            return sorted(self.__mem.keys())[-1] + 1

    def writenext(self, value):
        """
        Writes a value to the next available memory address.
        
        Args:
            value (int): The value to write to the memory.
        
        Raises:
            IndexError: If there are no available memory addresses.
        """
        next_addr = self.__next
        if next_addr not in Memory.ADDRESSABLE_SPACE:
            raise IndexError("No available memory address")
        self.write(next_addr, value)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.read(key)
        if isinstance(key, slice):
            return [self.read(i) for i in range(key.start, key.stop)]

    @staticmethod
    def __preview_lower_bound(center, size):
        lower = center - (size // 2)

        if lower not in Memory.ADDRESSABLE_SPACE:
            return Memory.ADDRESSABLE_SPACE.start
        else:
            return lower

    @staticmethod
    def __preview_upper_bound(center, size):
        upper = center + (size // 2) + 1

        if upper not in Memory.ADDRESSABLE_SPACE:
            return Memory.ADDRESSABLE_SPACE.stop
        else:
            return upper

    @staticmethod
    def __preview_range(center, size):
        lower = Memory.__preview_lower_bound(center, size)
        upper = Memory.__preview_upper_bound(center, size)
        offset = size // 2 ## The offset is how far away from the center the bounds move

        if (center - offset) not in Memory.ADDRESSABLE_SPACE:
            ## i.e. if the offset produces a value below zero
            #  add the remainder of the offset to the upper bound
            upper += abs(center - offset)

        if (center + offset) not in Memory.ADDRESSABLE_SPACE:
            ## i.e. if we the offset would overflow out of
            #  the addressable space, move the lower bound
            #  down so that it preserves the window size
            lower -= (center + offset) - Memory.ADDRESSABLE_SPACE.stop + 1

        return range(lower, upper)

    def preview(self, center, size=7):
        preview_range = Memory.__preview_range(center, size)

        preview = {}
        for address in preview_range:
            preview[address] = self[address]

        return preview

    def clear(self, new_mem=[]):
        """
        Clears the memory, optional parameter takes a list of Opcodes to store.
        """
        if len(new_mem) == 0:
            self.__mem = dict()
        elif len(new_mem) not in Memory.ADDRESSABLE_SPACE:
            raise IndexError(f"Attempted to clear memory with an array of length {len(new_mem)}. Cannot clear memory with an array whose length exceeds {Memory.ADDRESSABLE_SPACE.stop}")
        else:
            mem = dict()
            for i in range(len(new_mem)):
                if not isinstance(new_mem[i], Opcode):
                    raise TypeError(f"Attempted to clear memory with a non-Opcode object at index {i}")
                mem[i] = new_mem[i]
            self.__mem = mem