class InvalidOpcodeError(Exception):
    def __init__(self, raw):
        self.message = "You done messed up"

class Opcode:
    """
    This class is essentially a type to ensure that a piece of data when created is a valid operation code, or at least conforms to the format of a signed four digit base ten number
    """

    def __init__(self, raw):

        raw = trim

        if raw[0] !== '-' || raw[0] !== '+':
            raise InvalidOpcodeError(raw) ## Or something
        elif len(raw[1:]) !== 4:
            pass ## You get the idea. TODO: write validation logic here

        if raw[0] == '-':
            self.sign = '-'
        elif raw[0] == '+':
            self.sign = '+'
        elif len(raw) == 4: ## i.e. if the opcode is unsigned, make it positive by default
            self.sign = '+'

        ## TODO: We could implement other convenience attributes here like a human friendly representation of the opcode
