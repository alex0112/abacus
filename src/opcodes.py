class Opcode:
    """
    Class to represent an opcode in the simulator.
    """

    __op_list = {
            10: "READ", 11: "WRITE", 20: "LOAD", 21: "STORE",
            30: "ADD", 31: "SUBTRACT", 32: "DIVIDE", 33: "MULTIPLY",
            40: "BRANCH", 41: "BRANCHNEG", 42: "BRANCHZERO", 43: "HALT"
        }

    @staticmethod
    def __4_to_6(raw):
        if len(raw) == 6 or len(raw) == 7:
            return raw

        sign = raw[0]
        operation = raw[1:3]
        operand = raw[3:]

        if Opcode.__op_list.get(int(operation)) is None:
            return f"{sign}00{operation}{operand}"
    
        elif Opcode.__op_list.get(int(operation)):
            return f"{sign}0{operation}0{operand}"
        else:
            raise ValueError(f"Wasn't able to convert 4-digit(?) {raw} into 6-digit format.")

    def __init__(self, raw):
        """
        Initialize the Opcode with a raw string value.
        
        Args:
            raw (str): The raw string value of the opcode.
        
        Raises:
            ValueError: If the raw value is invalid.
        """
        if isinstance(raw, int):
            raw = f"{raw:+07d}"

        raw = raw.strip()

        if not raw:
            raise ValueError("Opcode cannot be empty")
        if raw[0] not in ['-', '+']:
            raw = '+' + raw

        if len(raw) == 4 or len(raw) == 5:
            raw = Opcode.__4_to_6(raw)
        
        if not raw[1:].isdigit() or len(raw[1:]) != 6:
            raise ValueError(f"Could not make opcode from {raw}. Opcode must be either 4 or 6 digits")

        try:
            self.__numeric = int(raw)
        except ValueError:
            raise ValueError(f"Could not make opcode from {raw}. Opcode must be either 4 or 6 digits")

        self.__raw = raw
        self.__sign = ""
        
    @property
    def name(self):
        """
        Returns the name of the operation corresponding to the opcode.
        """
        if self.raw[0].isdigit():
            self.__sign = "+"
            self.raw = "+" + self.raw
            self.__raw = new_raw
        operation = int(self.raw[1:4])
        return Opcode.__op_list.get(operation, "NOOP")

    @property
    def sign(self):
        """
        Returns the sign of the opcode.
        """
        self.__sign = self.raw[0]
        return self.__sign

    @property
    def operand(self):
        """
        Returns the operand of the opcode.
        """
        print(f"raw is: {self.raw}")
        return self.raw[4:]

    @property
    def raw(self):
        return self.__raw

    @property
    def numeric(self):
        return self.__numeric
    
    @property
    def human_friendly(self):
        if self.name == "NOOP":
            return self.name
        else:
            return f"{self.name} {self.operand}"

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
        raw_string = f"{int(raw_integer):+07d}"

        if raw_integer > 999999 or raw_integer < -999999:
            truncated  = raw_string[-6:] ## Grab the last six digits
            sign       = raw_string[0]
            overflowed = int(f"{sign}{truncated}")

            print(f"warning: overflowing {raw_string} to {overflowed:+07d}")
            
            return Opcode(f"{overflowed:+07d}")
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
    
