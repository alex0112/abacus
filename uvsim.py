#!/usr/bin/env python3

from src.cpu import CPU
from src.memory import Memory
from src.io_device import IODevice
from src.opcodes import Opcode

class UVSim:
    """
    An abstraction representing the UVSim virtual machine. It represents the current state of the virtual machine and creates its memory, register, and CPU.
    """
    def __init__(self, reader=None, writer=None, out_line=None):
        """
        Initialize and create a UVSim VM
        """
        self.__memory = Memory()
        self.__io  = IODevice(reader, writer)
        self.__cpu = CPU(out_line)

    @property
    def mem(self):
        return self.__memory

    @property
    def cpu(self):
        return self.__cpu

    @property
    def io_device(self):
        return self.__io

    def load(self, filename):
        """
        Given a filename load its contents into memory starting at location `00`
        """
        self.mem.clear()
        with open(filename) as program:
            #if len(program) > 100: ## TODO: write a check here for memory bounds
            #    pass ## TODO: We need to define behavior for when a program exceeds the available memory

            for line in program:
                opcode = Opcode(line)
                self.mem.writenext(opcode)

    def execute(self):
        """
        Walk through the contents of memory and hand each instruction to the CPU
        """
        #if len(self.mem) == 0:
        #pass ## TODO: define this behavior
        #else:
        try:
            self.cpu.run(self.mem, self.io_device, preview=True)
        except KeyboardInterrupt:
            print("\nAborting...")
            exit(0)

    def store(self, filename):
        """
        Store the contents of memory to a file
        """

        # Find the index of the last non-empty opcode
        last_non_empty_index = -1
        for i in range(len(self.mem) - 1, -1, -1):
            if str(self.mem[i]) != '+0000':
                last_non_empty_index = i
                break

        # Write opcodes to the file, including intermediate empty ones
        with open(filename, 'w') as program:
            for i, opcode in enumerate(self.mem):
                if i <= last_non_empty_index:
                    program.write(str(opcode) + "\n")


            
            print('Program saved successfully')
            
    def convert(self, filename):
        """
        Convert the contents of memory to a binary file
        """
        op_list = [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]
        new_list = []
        file_content = []
        if filename == "":
            print("Filename not provided")
            return
        try:
            with open(filename, 'r') as file:
                file_content = file.readlines()
                file = file_content[:]
                for line in file:
                    sign_flag = False
                    current = line.strip()
                    #check for line structure
                    if current[0] == "+" or current[0] == "-":
                        sign_flag = True
                        current = current[1:]
                    if len(current) <= 3:
                        for i in range(4-len(current)):
                            current = "0" + current
                        print("Some values where prepended with 0s")
                    elif len(current) > 4:
                        raise Exception("File contains invalid opcodes")
                    if int(current[:2]) in op_list and sign_flag:
                        current = f"{line[0]}0{current[0:2]}0{current[2:]}\n" #add a 0 to the opcode and 0 to the address
                    elif int(current[:2]) in op_list and not sign_flag:
                        current = f"+0{current[0:2]}0{current[2:]}\n"
                    elif sign_flag:
                        current = f"{line[0]}00{current}\n" #add 00 to the address if is just value
                    else:
                        current = f"+00{current}\n"
                    new_list.append(current)
            new_list[-1] = new_list[-1].strip()
            #save in file
            with open(filename, 'w') as file:
                for line in new_list:
                    file.write(line)
                print('Program converted successfully')
        except Exception as e:
            with open(filename, "w") as file:
                for line in file_content:
                    file.write(line)
                print(f'Error converting the program: {e}')
                    

        


