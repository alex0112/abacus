# src/io_device.py

class IODevice:
    """
    Class to represent an input/output device for the simulator.

    Three components:
    - Reader
    - Writer
    - Error

    
    """
    def __init__(self, reader=None, writer=None, err=None):
        self.__last_write = ""
        self.__last_read = ""
        self.__last_err = ""

        if reader is None:
            self.__reader = lambda: input(">>> ")  # Default to using input() if no reader is provided
        else:
            self.__reader = reader
        
        if writer is None:
            self.__writer = lambda x: print(x)  # Default to using print() if no writer is provided
        else:
            self.__writer = writer

        if err is None:
            self.__err = lambda x: print(x)
        else:
            self.__err = err

    @property
    def last_read(self):
        """
        Returns the last read input.
        """
        return self.__last_read


    @last_read.setter
    def last_read(self, val):
        self.__last_read = val

    @property
    def last_write(self):
        """
        Returns the last written output.
        """
        return self.__last_write

    @last_write.setter
    def last_write(self, val):
        self.__last_write = val

    @property
    def last_err(self):
        """
        Returns the last err output.
        """
        return self.__last_err

    @last_err.setter
    def last_err(self, val):
        self.__last_err = val

    def read(self):
        """
        Reads input using the reader function.
        """
        inp = self.__reader()
        print(f"got {inp} as input")
        self.last_read = inp
        return inp

    def write(self, data):
        """
        Writes output using the writer function.
        """
        self.last_write = data
        self.__writer(data)

    def err(self, data):
        """
        Writes output using the err function.
        """
        self.last_err = data
        self.__writer(data)
