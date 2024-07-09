#!/usr/bin/env python

from sys import argv
from src.opcodes import Opcode

def main():
    """
    Read a BasicML program and assemble it into executable machine code for the UVUSim CPU
    """
    if len(argv) != 2:
        print("Please specify a BasicML program to assemble")
        exit(1)

    input_filename = argv[1]
    program = read_file(input_filename)
    assemble(program, "a.out.basm")

def read_file(filename):
    """
    Given a filename as its input, take each line of the program and return a list of its instructions
    """
    code = []
    with open(filename, 'r') as program:
        for line in program:
            opcode = Opcode(line)
            code.append(opcode)

    return code


def assemble(program, filename):
    """
    Walk through a program in BasicML and translate each instruction into its machine code equivalent
    """
    with open(filename, 'w') as output_file:
        counter = 0
        for opcode in program:
            if opcode.name == "NOOP":
                output_file.write(f"{counter:02d} {opcode}\n")
            else:
                output_file.write(f"{counter:02d} {opcode.name} {opcode.operand}\n")
            counter += 1

    print(f"Wrote disassembled program to {filename}")

if __name__ == '__main__':
    main()
