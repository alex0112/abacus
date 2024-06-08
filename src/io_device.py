class IODevice:
    """
    Get user input/output
    """
    def __init__(self, reader=None, writer=None):
        self.__last_write = ""
        self.__last_read = ""

        if reader is None:
            self.__reader = lambda: input()
       
        if writer is None:
            self.__writer = lambda x: print(x)

    def read(self):
        inp = self.__reader()
        self.__last_read = inp

        return inp

    def write(self, data):
        self.__last_write = data
        self.__writer(data)
