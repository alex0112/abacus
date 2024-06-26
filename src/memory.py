from src.opcodes import Opcode

class Memory:
    """
    Class to represent the memory of the simulator.
    """
    ADDRESSABLE_SPACE = range(0, 100)
    
    def __init__(self, arr=[]):
        if len(arr) == 0:
            self.__mem = dict()
        else:
            mem = dict()
            for i in range(len(arr)):
                mem[i] = arr[i]
            self.__mem = mem
        
        #self.__mem = [0] * 100  # Initialize memory with 100 locations set to 0

    def __len__(self):
        """
        Returns the length of the memory.
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

        return self.__mem.get(address, Opcode("+0000"))

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
        ## The upper bound should be 

        upper = center + (size // 2) + 1

        if upper not in Memory.ADDRESSABLE_SPACE:
            return Memory.ADDRESSABLE_SPACE.stop
        else:
            return upper

    @staticmethod
    def __preview_range(center, size):
        lower = Memory.__preview_lower_bound(center, size)
        upper = Memory.__preview_upper_bound(center, size)
        offset = size // 2


        if (center - offset) != (center - lower):
            print(f"Upper: {upper} Lower: {lower}")
            print(f"Upper bound adjusted from {upper} to ", end='')
            upper += abs(center - offset)
            print(f"{upper}")

        # if center - (size //2) != (upper - center):
        #     print(f"Lower bound adjusted from {lower} to ", end='')
        #     lower -= (upper - center)
        #     print(f"{lower}")

        return range(lower, upper)

    def preview(self, center, size=3):
        preview_range = Memory.__preview_range(center, size)

        preview = {}

        for address in preview_range:
            preview[address] = self[address]

        return preview
