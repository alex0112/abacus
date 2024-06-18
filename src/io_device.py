# src/io_device.py

class IODevice:
    """
    Class to represent an input/output device for the simulator.
    """
    def __init__(self, reader=None, writer=None):
        self.__last_write = ""
        self.__last_read = ""

        if reader is None:
            self.__reader = lambda: input()  # Default to using input() if no reader is provided
        
        if writer is None:
            self.__writer = lambda x: print(x)  # Default to using print() if no writer is provided

    @property
    def last_read(self):
        """
        Returns the last read input.
        """
        return self.__last_read

    @property
    def last_write(self):
        """
        Returns the last written output.
        """
        return self.__last_write

    def read(self):
        """
        Reads input using the reader function.
        """
        inp = self.__reader()
        self.__last_read = inp
        return inp

    def write(self, data):
        """
        Writes output using the writer function.
        """
        self.__last_write = data
        self.__writer(data)