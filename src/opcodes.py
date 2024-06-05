class Opcode:
    '''This class is essentially a type to ensure that a piece of data 
    when created is a valid operation code, 
    or at least conforms to the format of a signed four digit base ten number'''

    def __init__(self, raw):
        self.__raw = raw
        self.__sign = ""
        self.__op_list = {10:"READ", 11:"WRITE", 20:"LOAD", 21:"STORE", 30:"ADD", 31:"SUBTRACT", 32:"DIVIDE", 33:"MULTIPLY", 40:"BRANCH", 41:"BRANCHNEG", 42:"BRANCHZERO", 43:"HALT"}

        if len(raw[1:]) != 4:
            raise ValueError("Opcode must only have 4 integers")
        if len(raw) == 4: ## i.e. if the opcode is unsigned, make it positive by default
            self.__sign = "+"

        ## TODO: We could implement other convenience attributes here like a human friendly representation of the opcode

    @property
    def name(self):
        #returns operation of the first 2 digits of raw opcode (10 returns READ)
        operation = int(self.raw[1:3])
        return self.__op_list.get(operation, "NOOP")

    @property
    def sign(self):
        #returns sign at the beginning of opcode(+,-)
        return self.__sign
    
    @property
    def operand(self):
        #returns operand or final 2 digits in raw opcode
        return self.raw[3:]
    
    def __str__(self):
        return self.raw
    
opcode = Opcode("+1042")
# opcode.operation()




    