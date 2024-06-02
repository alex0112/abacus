class InvalidOpcodeError(Exception):
    def __init__(self, raw):
        self.message = "You done messed up"

class Opcode:
    """
    This class is essentially a type to ensure that a piece of data when created is a valid operation code, or at least conforms to the format of a signed four digit base ten number
    """

    def __init__(self, raw):
        self.raw = raw

        if raw[0] != '-' and raw[0] != '+':
            raise ValueError("Must have a + or - at the beginning of opcode")
        elif len(raw[1:]) != 4:
            raise
        if raw[0] == '-':
            self.sign = '-'
        elif raw[0] == '+':
            self.sign = '+'
        elif len(raw) == 4: ## i.e. if the opcode is unsigned, make it positive by default
            self.sign = '+'

        ## TODO: We could implement other convenience attributes here like a human friendly representation of the opcode

    def operation(self):
        #returns operation of the first 2 digits of raw opcode (10 returns READ)
        pass

    def sign(self):
        #returns sign at the beginning of opcode(+,-)
        pass

    def operand(self):
        #returns operand or final 2 digits in raw opcode
        pass
