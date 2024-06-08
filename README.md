# Abacus - A UVSim Virtual Machine

UVSim Virtual Machine

![image](https://github.com/alex0112/abacus/assets/7142972/ea29fa8f-236c-4a23-92a1-361781afffa1)

## Milestone 2 Submission:

- Design Document: Our design document can be found in the [`Milestone_2/`](https://github.com/alex0112/abacus/tree/main/Milestone_2) directory. Additionally we describe additional program design in [ARCH.md](https://github.com/alex0112/abacus/blob/main/ARCH.md).
- Working Prototype: This repository.
- Unit Tests: Tests can be found in `test/` and run with `pytest`. See the tests section below for more details.
  - Table of test cases can be found in the `Milestone_2/` directory
- Other Documents: 
  - This README (you're reading it)
  - Meeting notes can be found in the `Milestone_2/`

## Running the Program

The most basic invocation of the program is:

```bash
python main.py <path_to_program>
```

It expects a program written in BasicML.

The program works best with `Python 3.12.0`. The official release for which can be found [here](https://www.python.org/downloads/release/python-3120/)

### Tests
Testing is handled through pytest. In order to ensure that the correct version of pytest is installed install the dependencies with `pip install -r requirements.txt`

At that point you should be able to run the tests from the root directory of this project with `make test` (on UNIX based systems) or by simply called `pytest` directly.

### Demo
In order to run a basic program (examples can be found in the `bml_examples/` directory) run

```bash
make demo
```

or if `make` is not available:

```bash
python main.py bml_examples/Test1.txt
```

## Architecture:
The general architecture of this system is described in [ARCH.md](https://github.com/alex0112/abacus/blob/main/ARCH.md)

## Project Requirements:
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

