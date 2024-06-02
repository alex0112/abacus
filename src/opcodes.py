class Opcode:
    '''This class is essentially a type to ensure that a piece of data 
    when created is a valid operation code, 
    or at least conforms to the format of a signed four digit base ten number'''

    def __init__(self, raw):
        self.raw = raw
        self.sign = ""

        if raw[0] != '-' and raw[0] != '+':
            raise ValueError("Must have a + or - at the beginning of opcode")
        if len(raw[1:]) != 4:
            raise ValueError("Opcode must only have 4 integers")
        if len(raw) == 4: ## i.e. if the opcode is unsigned, make it positive by default
            self.sign = "+"

        ## TODO: We could implement other convenience attributes here like a human friendly representation of the opcode

    def get_operation(self):
        #returns operation of the first 2 digits of raw opcode (10 returns READ)
        return self.raw[1:3]
         
    def get_sign(self):
        #returns sign at the beginning of opcode(+,-)
        return self.raw[0]

    def get_operand(self):
        #returns operand or final 2 digits in raw opcode
        return self.raw[3:]
    
    def __str__(self):
        return self.raw
    
opcode = Opcode("+1042")




    