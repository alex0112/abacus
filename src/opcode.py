#!/usr/bin/env python3

class Opcode:
    """
    This class is essentially a type to ensure that a piece of data when created is a valid operation code, or at least conforms to the format of a signed four digit base ten number
    """
    def __init__(self, raw):
        self.name = "BRANCH" ## Temporary default
        self.operand = 1


class InvalidOpcodeError(Exception):
    def __init__(self, raw):
        self.message = "You done messed up"
