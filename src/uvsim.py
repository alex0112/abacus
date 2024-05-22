#!/usr/bin/env python3

import CPU
import Memory

class UVSim:
    """
    An abstraction representing the UVSim virtual machine. It represents the current state of the virtual machine and creates its memory, register, and CPU.
    """
    def __init__():
        """
        Initialize and create a UVSim VM
        """
        self.__memory = Memory.new()
        self.__cpu = CPU.new()
