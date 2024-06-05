class InvalidOpcodeError(Exception):
    """
    Custom exception for invalid opcodes.
    """
    def __init__(self, raw):
        self.message = f"Invalid opcode: {raw}"
        super().__init__(self.message)

class Opcode:
    """
    This class ensures that a piece of data, when created, is a valid operation code,
    or at least conforms to the format of a signed four-digit base ten number.
    """
    def __init__(self, raw):
        raw = raw.strip()

        # Validate the opcode format
        if raw[0] not in ('-', '+'):
            raise InvalidOpcodeError(raw)  # Ensure the opcode starts with a sign
        elif len(raw[1:]) != 4:
            raise InvalidOpcodeError(raw)  # Ensure the opcode has four digits after the sign

        self.raw = raw
        self.sign = raw[0]
        self.value = int(raw)

    @classmethod
    def new(cls, raw_num):
        """
        Factory method to create a new Opcode instance.
        """
        return cls(raw_num)

    def __repr__(self):
        return f"Opcode({self.raw})"