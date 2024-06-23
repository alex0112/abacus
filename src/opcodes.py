class Opcode:
    """
    Class to represent an opcode in the simulator.
    """
    def __init__(self, raw):
        """
        Initialize the Opcode with a raw string value.
        
        Args:
            raw (str): The raw string value of the opcode.
        
        Raises:
            ValueError: If the raw value is invalid.
        """
        raw = raw.strip()
        if not raw:
            raise ValueError("Opcode cannot be empty")
        if raw[0] not in ['-', '+']:
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
        """
        Returns the name of the operation corresponding to the opcode.
        """
        if self.__raw[0].isdigit():
            self.__sign = "+"
            new_raw = "+" + self.__raw
            self.__raw = new_raw
        operation = int(self.__raw[1:3])
        return self.__op_list.get(operation, "NOOP")

    @property
    def sign(self):
        """
        Returns the sign of the opcode.
        """
        self.__sign = self.__raw[0]
        return self.__sign

    @property
    def operand(self):
        """
        Returns the operand of the opcode.
        """
        return self.__raw[3:]

    @property
    def raw(self):
        return self.__raw

    @property
    def numeric(self):
        return self.__numeric

    def __str__(self):
        """
        Returns the string representation of the opcode.
        """
        return self.__raw

    @staticmethod
    def __overflow(raw_integer):
        """
        The behavior implemented here should define how an Opcode is expected to handle overflow or underflow behavior

        The current specification is:
        "Truncate overflows (so same sign, just drop the extra digits, keep the last four)"
        """
        raw_string = f"{int(raw_integer):+05d}"
        print(f"Handling overflow for {raw_string}")

        if raw_integer > 9999 or raw_integer < -9999:
            truncated = raw_string[-4:] ## Grab the last four digits
            sign      = raw_string[0]
            
        
            overflowed = int(f"{sign}{truncated}")
            print(f"truncated: {truncated}")
            print(f"sign: {sign}")

            
            return Opcode(f"{overflowed:+05d}")
        else:
            return Opcode(raw_string)
            
    def __eq__(self, other):
        """
        Checks if two opcodes are equal.
        """
        if isinstance(other, Opcode):
            return self.numeric == other.numeric
        if isinstance(other, int):
            return self.numeric == other

        return False

    def __add__(self, other):
        """
        Adds two opcodes.
        
        Args:
            other (Opcode): The other opcode to add.
        
        Returns:
            Opcode: The resulting opcode from the addition.
        
        Raises:
            OverflowError: If the resulting value is out of bounds.
        """
        if isinstance(other, Opcode):
            result = self.numeric + other.numeric
            return Opcode.__overflow(result)

        return NotImplemented

    def __sub__(self, other):
        """
        Subtracts two opcodes.
        
        Args:
            other (Opcode): The other opcode to subtract.
        
        Returns:
            Opcode: The resulting opcode from the subtraction.
        
        Raises:
            OverflowError: If the resulting value is out of bounds.
        """
        if isinstance(other, Opcode):
            result = self.numeric - other.numeric
            return Opcode.__overflow(result)

        return NotImplemented

    def __mul__(self, other):
        """
        Multiplies two opcodes.
        
        Args:
            other (Opcode): The other opcode to multiply.
        
        Returns:
            Opcode: The resulting opcode from the multiplication.
        
        Raises:
            OverflowError: If the resulting value is out of bounds.
        """
        if isinstance(other, Opcode):
            result = self.numeric * other.numeric
            return Opcode.__overflow(result)

        return NotImplemented

    def __truediv__(self, other):
        """
        Divides two opcodes.
        
        Args:
            other (Opcode or int): The other opcode or integer to divide by.
        
        Returns:
            Opcode: The resulting opcode from the division.
        
        Raises:
            ZeroDivisionError: If division by zero is attempted.
        """
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
