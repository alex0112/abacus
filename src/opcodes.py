class Opcode:
    '''This class is essentially a type to ensure that a piece of data 
    when created is a valid operation code, 
    or at least conforms to the format of a signed four digit base ten number'''

    def __init__(self, raw):
        if raw[0] not in ['-', '+']:
                # Prepend a + sign if the first character is not a sign
                raw = '+' + raw
                if len(raw[1:]) != 4:
                    raise ValueError("Opcode must be 4 digits")
        else:
            if len(raw[1:]) != 4:
                    raise ValueError("Opcode must be 4 digits")

        self.__raw = raw
        self.__sign = ""
        self.__op_list = {10:"READ", 11:"WRITE", 20:"LOAD", 21:"STORE", 30:"ADD", 31:"SUBTRACT", 32:"DIVIDE", 33:"MULTIPLY", 40:"BRANCH", 41:"BRANCHNEG", 42:"BRANCHZERO", 43:"HALT"}

    @property
    def name(self):
        if self.__raw[0].isdigit():
            self.__sign = "+"
            new_raw = "+" + self.__raw
            self.__raw == new_raw

        #returns operation of the first 2 digits of raw opcode (10 returns READ)
        operation = int(self.__raw[1:3])
        return self.__op_list.get(operation, "NOOP")

    @property
    def sign(self):
        self.__sign = self.__raw[0]
        #returns sign at the beginning of opcode(+,-)
        return self.__sign
    
    @property
    def operand(self):
        #returns operand or final 2 digits in raw opcode
        return self.__raw[3:]
    
    def __str__(self):
        return self.__raw
    






    