"""
A BasicML assembler.

This executable accepts a BasicML program as its input and produces an assembled selection of machine code for the UVSim CPU.

Usage:

```
$ basm foo.bml
Working...
Wrote assembled program to foo.basm
```
"""

from sys import argv

def main():
    """
    Read a BasicML program and assemble it into executable machine code for the UVUSim CPU
    """
    if len(argv) != 2:
        print("Please specify a BasicML program to assemble")
        exit(1)

    filename = argv[0]
    program = read_file(filename)
    assemble(program, filename)

def read_file(filename):
    """
    Given a filename as its input, take each line of the program and return a list of its instructions
    """
    with open(filename) as program:
        pass

def assemble(program, filename):
    """
    Walk through a program in BasicML and translate each instruction into its machine code equivalent
    """
    pass

if __name__ == '__main__':
    main()
