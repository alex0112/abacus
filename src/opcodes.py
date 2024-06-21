class Opcode:
    '''This class is essentially a type to ensure that a piece of data 
    when created is a valid operation code, 
    or at least conforms to the format of a signed four digit base ten number'''

    def __init__(self, raw):
        raw = raw.strip()

        if not raw:
            raise ValueError("Opcode cannot be empty")
        if raw[0] not in ['-', '+']:
            # Prepend a + sign if the first character is not a sign
            raw = '+' + raw
        if not raw[1:].isdigit() or len(raw[1:]) != 4:
            raise ValueError(f"Could not make opcode from {raw}. Opcode must be 4 digits")
        self.__raw = raw
        self.__sign = ""
        self.__op_list = {
            10: "READ", 11: "WRITE", 20: "LOAD", 21: "STORE", 
            30: "ADD", 31: "SUBTRACT", 32: "DIVIDE", 33: "MULTIPLY",
            40: "BRANCH", 41: "BRANCHNEG", 42: "BRANCHZERO", 43: "HALT"
        }

    @property
    def name(self):
        if self.__raw[0].isdigit():
            self.__sign = "+"
            new_raw = "+" + self.__raw
            self.__raw = new_raw

        # Returns operation of the first 2 digits of raw opcode (10 returns READ)
        operation = int(self.__raw[1:3])
        return self.__op_list.get(operation, "NOOP")

    @property
    def sign(self):
        self.__sign = self.__raw[0]
        # Returns sign at the beginning of opcode(+,-)
        return self.__sign
    
    @property
    def operand(self):
        # Returns operand or final 2 digits in raw opcode
        return self.__raw[3:]
    
    def __str__(self):
        return self.__raw

    # Implementing equality and arithmetic operations
    def __eq__(self, other):
        if isinstance(other, Opcode):
            return self.__raw == other.__raw
        return False

    def __add__(self, other):
        if isinstance(other, Opcode):
            result = int(self.__raw) + int(other.__raw)
            if result > 9999 or result < -9999:
                raise OverflowError("Resulting opcode is out of bounds")
            return Opcode(f"{result:+05d}")
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Opcode):
            result = int(self.__raw) - int(other.__raw)
            if result > 9999 or result < -9999:
                raise OverflowError("Resulting opcode is out of bounds")
            return Opcode(f"{result:+05d}")
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Opcode):
            result = int(self.__raw) * int(other.__raw)
            if result > 9999 or result < -9999:
                raise OverflowError("Resulting opcode is out of bounds")
            return Opcode(f"{result:+05d}")
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Opcode):
            if int(other.__raw) == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = int(self.__raw) // int(other.__raw)
            return Opcode(f"{result:+05d}")
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = int(self.__raw) // other
            return Opcode(f"{result:+05d}")
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Opcode):
            return int(self.__raw) < int(other.__raw)
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Opcode):
            return int(self.__raw) > int(other.__raw)
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Opcode):
            return int(self.__raw) <= int(other.__raw)
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Opcode):
            return int(self.__raw) >= int(other.__raw)
        return NotImplemented




