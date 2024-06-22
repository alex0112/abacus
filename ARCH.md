# Proposed Architecture of UVSim machine

High level overview of the design of our machine. This is just a draft, so nothing here is set in stone.

### Project Organization:

Bird's eye view:
```
├── README.md    ## The README
├── ARCH.md      ## You're reading it
│
├── bml_examples ## Example programs for test cases
│   └── ...
├── test         ## Unit Tests
│   └── ...
│
├── src
│   ├── cpu.py       ## An abstraction representing the CPU and its single register, processes opcodes and modifies memory
│   ├── io_device.py ## Represents input and output to the console (wanted to separate this for testing)
│   ├── memory.py    ## The program memory, has methods for addressing and checks against overflowing available memory
│   └── opcode.py    ## Basically a type that processes and reads an opcode like `+1007` and makes sure that it's valid.
│
├── basm.py  ## An optional program that turns the human friendly representation of of BasicML into numbers
├── uvsim.py ## The main abstraction which integrates the memory/cpu/io etc. into one object
├── gui.py  ## A graphical user interface for UVSim that allows users to load, execute, and debug BasicML programs interactively
└── main.py  ## Bootstrap everything and get it running

```

#### Files:

##### `uvsim.py`:

This program integrates the memory, CPU, and IO device together into one blob. It loads programs into its memory and then processes them with the CPU:

```python
    def execute(self):
        """
        Walk through the contents of memory and hand each instruction to the CPU
        """
        if len(self.mem) == 0:
            pass ## TODO: define this behavior
        else:
            for raw_num in self.mem:
                opcode = Opcode.new(raw_num) ## see opcode.py

                self.cpu.process(opcode, self.mem, self.io_device)
```

##### `src/cpu.py`:

This is an abstraction of the processor, and it has a function called `process()`:

```python
     def process(self, opcode, memory, io_device):
        """
        Given an opcode, memory object, and peripherals, modify the memory according to the instruction and value given
        """
        ...
```

It takes an `Opcode` and a `Memory` object as input and modifies the memory according to whatever the instruction in the `Opcode` is.

##### `src/memory.py`:
    
This file provides some utilities for:

- writing data to specific locations in memory
- if a location doesn't exist yet then it creates it and any intermediary addresses
- if we get to location `99` the machine is out of memory, so it yells at the user at this point or something

##### `src/opcode.py`:

This is just a little object to represent an opcode/piece of memory. I'm not married to using it, but I was envisioning some utility methods to get the sign of the number that's it represents and some exceptions for when a program with an invalid opcode is passed in.


