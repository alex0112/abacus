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

    def __str__(self):
        """
        Returns the string representation of the opcode.
        """
        return self.__raw

    def __eq__(self, other):
        """
        Checks if two opcodes are equal.
        """
        if isinstance(other, Opcode):
            return self.__raw == other.__raw
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
            result = int(self.__raw) + int(other.__raw)
            if result > 9999 or result < -9999:
                raise OverflowError("Resulting opcode is out of bounds")
            return Opcode(f"{result:+05d}")
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
            result = int(self.__raw) - int(other.__raw)
            if result > 9999 or result < -9999:
                raise OverflowError("Resulting opcode is out of bounds")
            return Opcode(f"{result:+05d}")
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
            result = int(self.__raw) * int(other.__raw)
            if result > 9999 or result < -9999:
                raise OverflowError("Resulting opcode is out of bounds")
            return Opcode(f"{result:+05d}")
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