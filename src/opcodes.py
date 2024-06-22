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

        try:
            self.__numeric = int(raw)
        except ValueError:
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
    

    @property
    def raw(self):
        return self.__raw

    @property
    def numeric(self):
        return self.__numeric

    def __str__(self):
        return self.__raw

    @staticmethod
    def __overflow(raw_integer):
        """
        The behavior implemented here should define how an Opcode is expected to handle overflow or underflow behavior

        The current specification is:
        "Truncate overflows (so same sign, just drop the extra digits, keep the last four)"
        """
        raw_string = f"{int(raw_integer):+05d}"

        if raw_integer > 9999 or raw_integer < -9999:
            truncated = raw_string[:-4] ## Grab the last four digits
            sign      = raw_string[0]

            return Opcode(f"{int(truncated):+05d}")
        else:
            return Opcode(raw_string)
            
    def __eq__(self, other):
        if isinstance(other, Opcode):
            return self.numeric == other.numeric
        if isinstance(other, int):
            return self.numeric == other

        return False

    def __add__(self, other):
        if isinstance(other, Opcode):
            result = self.numeric + other.numeric
            return Opcode.__overflow(result)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Opcode):
            result = self.numeric - other.numeric
            return Opcode.__overflow(result)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Opcode):
            result = self.numeric * other.numeric
            return Opcode.__overflow(result)

        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Opcode):
            if other.numeric == 0:
                raise ZeroDivisionError("Cannot divide by zero")
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            
        if isinstance(other, Opcode):
            result = self.numeric // other.numeric
            return Opcode.__overflow(result)
        elif isinstance(other, int):
            result = self.numeric // other
            return Opcode.__overflow(result)
            
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Opcode):
            if other.numeric == 0:
                raise ZeroDivisionError("Cannot divide by zero")
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            
        if isinstance(other, Opcode):
            result = self.numeric // other.numeric
            return Opcode.__overflow(result)
        elif isinstance(other, int):
            result = self.numeric // other
            return Opcode.__overflow(result)
            
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Opcode):
            return int(self.numeric) < other.numeric
        elif isinstance(other, int):
            return self.numeric < other

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Opcode):
            return self.numeric > other.numeric
        elif isinstance(other, int):
            return self.numeric > other

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Opcode):
            return int(self.numeric) <= other.numeric
        elif isinstance(other, int):
            return self.numeric <= other

        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Opcode):
            return int(self.numeric) >= other.numeric
        elif isinstance(other, int):
            return self.numeric >= other

        return NotImplemented
