# Abacus - A UVSim Virtual Machine and Assembler

The UVSim is a simple virtual machine, but powerful. The UVSim can only interpret a machine language called BasicML.

The UVSim contains *CPU*, *register*, and *main memory*. An *accumulator* – a register into which information is put before the UVSim uses it in calculations or examines it in various ways. All the information in the UVSim is handled in terms of words. A word is a signed four-digit decimal number, such as +1234, -5678. The UVSim is equipped with a 100-word memory, and these words are referenced by their location numbers 00, 01, ..., 99. The BasicML program must be loaded into the main memory starting at location 00 before executing. Each instruction written in BasicML occupies one word of the UVSim memory (instruction are signed four-digit decimal number). We shall assume that the sign of a BasicML instruction is always plus, but the sign of a data word may be either plus or minus. Each location in the UVSim memory may contain an instruction, a data value used by a program or an unused area of memory. The first two digits of each BasicML instruction are the operation code specifying the operation to be performed.

BasicML vocabulary defined as follows:

### I/O operation:

- `READ = 10`  Read a word from the keyboard into a specific location in memory.
- `WRITE = 11` Write a word from a specific location in memory to screen.

### Load/store operations:

- `LOAD = 20` Load a word from a specific location in memory into the accumulator.
- `STORE = 21` Store a word from the accumulator into a specific location in memory.

### Arithmetic operation:

- `ADD = 30` Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
- `SUBTRACT = 31` Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
- `DIVIDE = 32` Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
- `MULTIPLY = 33` multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

### Control operation:

- `BRANCH = 40` Branch to a specific location in memory
- `BRANCHNEG = 41` Branch to a specific location in memory if the accumulator is negative.
- `BRANCHZERO = 42` Branch to a specific location in memory if the accumulator is zero.
- `HALT = 43` Stop the program

The last two digits of a BasicML instruction are the operand – the address of the memory location containing the word to which the operation applies.

## Proposed Architecture:

See [ARCH.md](https://github.com/alex0112/abacus/blob/main/ARCH.md)
